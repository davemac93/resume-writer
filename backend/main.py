from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from lib.agent import run_agent

def create_default_profile_template(user_info: dict) -> dict:
    """Create a default profile template for new users"""
    return {
        "personal_info": {
            "full_name": user_info.get("full_name", ""),
            "email": user_info.get("email", ""),
            "phone": "",
            "linkedin_url": "",
            "location": ""
        },
        "personal_summary": "",
        "work_experience": [],
        "education": [],
        "skills": {
            "technical_skills": [],
            "process_project_skills": [],
            "languages": []
        },
        "certifications": [],
        "projects": [],
        "interests": []
    }
from auth import get_current_user
from database_supabase_api import supabase_db_manager as db_manager
from html_pdf_generator import html_pdf_generator, cleanup_playwright
from flexible_resume_processor import FlexibleResumeProcessor
from storage import storage_manager
import asyncio
import json
import uuid
import io
import os
import signal
import sys
from typing import Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting CV Builder API...")
    
    if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
        print("✅ Supabase configured")
    else:
        print("⚠️  Supabase not configured - some features will be disabled")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down CV Builder API...")
    try:
        await asyncio.wait_for(cleanup_playwright(), timeout=15.0)
        print("✅ Cleanup completed successfully")
    except asyncio.TimeoutError:
        print("⚠️  Cleanup timed out, forcing shutdown")
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
    finally:
        print("🛑 Shutdown complete")

app = FastAPI(
    title="CV Builder API",
    description="AI-powered CV generation and management",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "CV Builder API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/generate-ai-flexible-cv/")
async def generate_ai_flexible_cv(
    job_offer_url: str = Form(...),
    profile_json: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Generate CV using AI agent + flexible parser workflow: JSON profile → AI agent → markdown → flexible parser → PDF"""
    try:
        print(f"🎯 Generating AI flexible CV for user {current_user['id']}")
        print(f"🔗 Job offer URL: {job_offer_url}")
        
        # Read and parse JSON profile
        profile_content = await profile_json.read()
        profile_data = json.loads(profile_content.decode('utf-8'))
        
        print(f"📄 Profile data keys: {list(profile_data.keys())}")
        
        # Step 1: Use AI agent to generate markdown from JSON profile
        print("🤖 Step 1: AI Agent generating markdown from JSON profile...")
        markdown_content = await run_agent(profile_data, job_offer_url)
        
        if not markdown_content:
            raise HTTPException(status_code=500, detail="AI agent failed to generate markdown")
        
        print(f"✅ AI agent generated markdown: {len(markdown_content)} characters")
        print(f"📝 Markdown preview: {markdown_content[:200]}...")
        
        # Step 2: Use flexible parser to process markdown
        print("🔧 Step 2: Flexible parser processing markdown...")
        processor = FlexibleResumeProcessor()
        structured_data = processor.process_resume_content(markdown_content, profile_json)
        
        print(f"✅ Processed data keys: {list(structured_data.keys())}")
        print(f"📊 Experience entries: {len(structured_data.get('experience', []))}")
        print(f"🏷️  Tags: {len(structured_data.get('tags', []))}")
        print(f"🎓 Education entries: {len(structured_data.get('education', []))}")
        print(f"📜 Certifications: {len(structured_data.get('certifications', []))}")
        print(f"🚀 Projects: {len(structured_data.get('projects', []))}")
        
        # Step 3: Generate PDF using template
        print("🎨 Step 3: Rendering template...")
        template_path = "resume_template.html"
        if not os.path.exists(template_path):
            raise HTTPException(status_code=500, detail="Template file not found")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Simple template processing
        html_content = template_content
        for key, value in structured_data.items():
            if isinstance(value, str):
                html_content = html_content.replace(f'{{{{{key}}}}}', value)
            elif isinstance(value, (int, float)):
                html_content = html_content.replace(f'{{{{{key}}}}}', str(value))
            elif value is None:
                html_content = html_content.replace(f'{{{{{key}}}}}', '')
        
        # Check if template syntax is still present
        if "{{" in html_content and "}}" in html_content:
            print("❌ Template syntax still present in rendered HTML!")
            lines = html_content.split('\n')
            for i, line in enumerate(lines):
                if "{{" in line and "}}" in line:
                    print(f"  Line {i+1}: {line.strip()}")
            raise HTTPException(status_code=500, detail="Template syntax not fully processed")
        else:
            print("✅ Template syntax successfully processed!")
        
        # Step 4: Generate PDF using Playwright
        print("📄 Step 4: Generating PDF with Playwright...")
        pdf_bytes = await html_pdf_generator.generate_pdf_from_html(html_content, current_user['id'])
        
        if not pdf_bytes:
            raise HTTPException(status_code=500, detail="PDF generation failed")
        
        print(f"✅ PDF generated successfully: {len(pdf_bytes)} bytes")
        
        # Step 5: Store in database
        print("💾 Step 5: Storing in database...")
        resume_id = str(uuid.uuid4())
        
        # Store PDF in Supabase Storage
        storage_url = await storage_manager.upload_pdf(pdf_bytes, current_user['id'], resume_id)
        
        if not storage_url:
            raise HTTPException(status_code=500, detail="Failed to store PDF")
        
        print(f"✅ PDF stored successfully: {storage_url}")
        
        # Store resume metadata in database
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            try:
                await db_manager.save_resume_metadata(current_user['id'], resume_id, job_offer_url)
                print("✅ Resume metadata saved")
            except Exception as e:
                print(f"⚠️  Failed to save resume metadata: {e}")
            
            try:
                await db_manager.update_resume_storage_url(current_user['id'], resume_id, storage_url)
                print("✅ Resume storage URL updated in database")
            except Exception as e:
                print(f"⚠️  Failed to update resume storage URL: {e}")
        else:
            print("⚠️  Database not configured - resume metadata not saved")
        
        return {
            "message": "AI Flexible CV generated and stored successfully",
            "storage_url": storage_url,
            "resume_id": resume_id,
            "resume": markdown_content  # Return the generated markdown for display
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"❌ Error generating AI flexible CV: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating AI flexible CV: {str(e)}")

@app.post("/validate-url/")
async def validate_url(
    request: dict,
    current_user: dict = Depends(get_current_user)
):
    """Validate URL accessibility and extract metadata"""
    try:
        url = request.get("url", "").strip()
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        # Add protocol if missing
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            print(f"🔧 Added https:// protocol to URL: {url}")
        
        # Basic URL format validation
        if not url.startswith(("http://", "https://")):
            raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
        
        # Special handling for LinkedIn URLs
        if 'linkedin.com/jobs' in url:
            print(f"✅ LinkedIn job URL detected: {url}")
            return {
                "url": url,
                "accessible": True,
                "title": "LinkedIn Job Posting",
                "description": "LinkedIn job URL validated"
            }
        
        # For now, we'll do basic validation
        # In a real implementation, you'd make an HTTP request to check accessibility
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Simulate metadata extraction
        metadata = {
            "url": url,
            "accessible": True,
            "title": "Job Posting",
            "description": "Job posting URL validated successfully"
        }
        
        return metadata
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error validating URL: {e}")
        raise HTTPException(status_code=500, detail=f"URL validation failed: {str(e)}")

@app.post("/validate-profile/")
async def validate_profile(
    request: dict,
    current_user: dict = Depends(get_current_user)
):
    """Validate JSON profile completeness and structure"""
    try:
        profile = request.get("profile", {})
        if not profile:
            raise HTTPException(status_code=400, detail="Profile data is required")
        
        # Required fields validation - check personal_info structure
        personal_info = profile.get("personal_info", {})
        required_fields = ["full_name", "email"]
        missing_fields = []
        
        for field in required_fields:
            if not personal_info.get(field):
                missing_fields.append(f"personal_info.{field}")
        
        if missing_fields:
            return {
                "valid": False,
                "missing_fields": missing_fields,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }
        
        # Optional but recommended fields
        recommended_fields = [
            "personal_info.phone", 
            "personal_summary", 
            "work_experience", 
            "education"
        ]
        missing_recommended = []
        
        for field in recommended_fields:
            if "." in field:
                # Nested field
                parts = field.split(".")
                if len(parts) == 2:
                    parent, child = parts
                    if not profile.get(parent, {}).get(child):
                        missing_recommended.append(field)
            else:
                # Top-level field
                if not profile.get(field):
                    missing_recommended.append(field)
        
        message = "Profile is valid and complete"
        if missing_recommended:
            message += f". Consider adding: {', '.join(missing_recommended)}"
        
        return {
            "valid": True,
            "missing_fields": [],
            "missing_recommended": missing_recommended,
            "message": message
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error validating profile: {e}")
        raise HTTPException(status_code=500, detail=f"Profile validation failed: {str(e)}")

@app.post("/generate-resume-agent/")
async def generate_resume_agent(
    request: dict,
    current_user: dict = Depends(get_current_user)
):
    """Generate resume using agent1 and flexible processor"""
    try:
        profile = request.get("profile", {})
        job_description = request.get("job_description", "")
        
        if not profile:
            raise HTTPException(status_code=400, detail="Profile data is required")
        
        if not job_description or len(job_description.strip()) < 50:
            raise HTTPException(status_code=400, detail="Job description is required and must be at least 50 characters")
        
        print(f"🎯 Generating resume with Agent 1 and flexible processor for user {current_user['id']}")
        print(f"📝 Job description length: {len(job_description)} characters")
        
        # Convert profile to JSON string for agent
        import json
        profile_json = json.dumps(profile, ensure_ascii=False)
        
        # Use Agent 1
        print("🤖 Using Agent 1...")
        markdown_content = await run_agent(profile_json, job_description)
        
        if not markdown_content:
            raise HTTPException(status_code=500, detail="Agent failed to generate markdown")
        
        print(f"✅ Agent generated markdown: {len(markdown_content)} characters")
        
        # Process with flexible parser
        print("🔧 Processing with flexible parser...")
        # Debug: Print profile structure
        print(f"📊 Profile structure: {list(profile.keys())}")
        if 'personal_info' in profile:
            print(f"📊 Personal info: {list(profile['personal_info'].keys())}")
        
        processor_obj = FlexibleResumeProcessor()
        structured_data = processor_obj.process_resume_content(markdown_content, profile)
        
        # Ensure contact info from profile takes priority over markdown extraction
        if 'personal_info' in profile:
            personal_info = profile['personal_info']
            structured_data.update({
                'name': personal_info.get('full_name', structured_data.get('name', '')),
                'title': personal_info.get('title', '') or personal_info.get('job_title', '') or structured_data.get('title', ''),
                'email': personal_info.get('email', structured_data.get('email', '')),
                'phone': personal_info.get('phone', structured_data.get('phone', '')),
                'location': personal_info.get('location', structured_data.get('location', '')),
                'linkedin': personal_info.get('linkedin_url', '') or personal_info.get('linkedin', '') or structured_data.get('linkedin', ''),
                'github': personal_info.get('github_url', '') or personal_info.get('github', '') or structured_data.get('github', '')
            })
        
        # Debug: Print extracted contact info
        print(f"📞 Extracted contact info: name='{structured_data['name']}', email='{structured_data['email']}', phone='{structured_data['phone']}', location='{structured_data['location']}'")
        
        # Generate PDF
        print("🎨 Generating PDF...")
        template_path = "resume_template.html"
        if not os.path.exists(template_path):
            raise HTTPException(status_code=500, detail="Template file not found")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Handlebars template processing
        from pybars import Compiler
        compiler = Compiler()
        template = compiler.compile(template_content)
        html_content = template(structured_data)
        
        # Generate PDF using Playwright
        pdf_bytes = await html_pdf_generator.generate_pdf_from_html(html_content, current_user['id'])
        
        if not pdf_bytes:
            raise HTTPException(status_code=500, detail="PDF generation failed")
        
        # Store in database
        resume_id = str(uuid.uuid4())
        storage_url = await storage_manager.upload_pdf(pdf_bytes, current_user['id'], resume_id)
        
        if not storage_url:
            raise HTTPException(status_code=500, detail="Failed to store PDF")
        
        # Store resume metadata
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            try:
                await db_manager.save_resume_metadata(current_user['id'], resume_id, job_description[:100] + "..." if len(job_description) > 100 else job_description)
                await db_manager.update_resume_storage_url(current_user['id'], resume_id, storage_url)
            except Exception as e:
                print(f"⚠️  Failed to save resume metadata: {e}")
        
        return {
            "message": "Resume generated successfully using Agent 1",
            "markdown": markdown_content,
            "resume": markdown_content,  # For backward compatibility
            "resume_id": resume_id,
            "storage_url": storage_url,
            "agent_used": "agent1"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generating resume: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")

# Profile completion endpoint removed - functionality not needed

# Profile response processing endpoint removed - functionality not needed

@app.post("/create-default-profile/")
async def create_default_profile_endpoint(
    current_user: dict = Depends(get_current_user)
):
    """Create a default profile template for new users"""
    try:
        print(f"👤 Creating default profile for user {current_user['id']}")
        
        # Extract user info from current_user
        print(f"🔍 User data structure: {current_user}")
        user_metadata = current_user.get("user_metadata", {})
        print(f"🔍 User metadata: {user_metadata}")
        
        # Try to get full_name from various possible locations
        full_name = (
            user_metadata.get("full_name") or 
            user_metadata.get("name") or 
            user_metadata.get("display_name") or 
            current_user.get("email", "").split("@")[0] or 
            "User"
        )
        
        user_info = {
            "full_name": full_name,
            "email": current_user.get("email", "")
        }
        
        print(f"🔍 Extracted user info: {user_info}")
        
        # Create default profile template
        default_profile = create_default_profile_template(user_info)
        
        # Save to database if configured
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            try:
                await db_manager.upsert_profile(current_user['id'], default_profile)
                print("✅ Default profile saved to database")
            except Exception as e:
                print(f"⚠️  Failed to save default profile to database: {e}")
        
        return {
            "message": "Default profile created successfully",
            "profile": default_profile
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error creating default profile: {e}")
        raise HTTPException(status_code=500, detail=f"Default profile creation failed: {str(e)}")

# Profile validation endpoint removed - functionality not needed

@app.get("/profile")
async def get_profile_endpoint(
    current_user: dict = Depends(get_current_user)
):
    """Get user profile from database"""
    try:
        print(f"🔍 Getting profile for user {current_user['id']}")
        
        if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            raise HTTPException(status_code=404, detail="Database not configured")
        
        # Get profile from database
        profile_data = await db_manager.get_profile(current_user['id'])
        
        if not profile_data:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        print(f"✅ Profile found for user {current_user['id']}")
        return profile_data.get('profile', {})
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting profile: {e}")
        raise HTTPException(status_code=500, detail=f"Profile retrieval failed: {str(e)}")

@app.post("/upsert-profile/")
async def upsert_profile_exact_endpoint(
    request: dict,
    current_user: dict = Depends(get_current_user)
):
    """Save the provided profile JSON to the database EXACTLY as given (no mutation)."""
    try:
        profile = request.get("profile", {})
        if not profile or not isinstance(profile, dict):
            raise HTTPException(status_code=400, detail="Profile data is required and must be an object")

        # Save to database if configured
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            try:
                await db_manager.upsert_profile(current_user['id'], profile)
                print("✅ Exact profile saved to database")
            except Exception as e:
                print(f"⚠️  Failed to save exact profile to database: {e}")
                raise HTTPException(status_code=500, detail="Failed to save profile to database")

        return {
            "message": "Profile saved successfully",
            "profile": profile
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error saving exact profile: {e}")
        raise HTTPException(status_code=500, detail=f"Profile save failed: {str(e)}")

# LinkedIn profile creation endpoint removed - functionality not needed

# Global variable to track shutdown
shutdown_event = asyncio.Event()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print(f"\n🛑 Received signal {signum}, initiating graceful shutdown...")
    shutdown_event.set()

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    import uvicorn
    
    # Configure uvicorn with proper shutdown handling
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True,
        timeout_keep_alive=30,
        timeout_graceful_shutdown=15
    )
    
    server = uvicorn.Server(config)
    
    try:
        server.run()
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt received, shutting down...")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        print("🛑 Server stopped")
