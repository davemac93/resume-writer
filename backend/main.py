from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from lib.agent import run_agent
from auth import get_user_from_token
from database_supabase_api import supabase_db_manager as db_manager
from pdf_generator import ResumePDFGenerator
from html_pdf_generator import html_pdf_generator, cleanup_playwright
from resume_processor import ResumeProcessor
from template_engine import template_engine
from storage import storage_manager
import asyncio
import json
import uuid
import io
import os
from typing import Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting CV Builder API...")
    
    if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
        try:
            await db_manager.init_pool()
            print("✅ Supabase API connection initialized")
        except Exception as e:
            print(f"⚠️  Supabase API connection failed: {e}")
            print("   Running without database features")
    
    # Initialize Playwright
    try:
        await html_pdf_generator.initialize()
        print("✅ Playwright browser initialized")
    except Exception as e:
        print(f"⚠️  Playwright initialization failed: {e}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down CV Builder API...")
    
    # Close Playwright browser
    try:
        await cleanup_playwright()
        print("✅ Playwright browser closed")
    except Exception as e:
        print(f"⚠️  Error closing Playwright: {e}")
    
    # Close database connection
    try:
        await db_manager.close_pool()
        print("✅ Database connection closed")
    except Exception as e:
        print(f"⚠️  Error closing database: {e}")

app = FastAPI(title="CV Builder API", version="1.0.0", lifespan=lifespan)

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_current_user(authorization: str = Header(None)):
    """Get current authenticated user from JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        scheme, token = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    return await get_user_from_token(token)

@app.get("/")
async def root():
    return {"message": "CV Builder API", "version": "1.0.0"}

@app.post("/debug-html-pdf/")
async def debug_html_pdf(resume_content: str = Form(...)):
    """Debug endpoint for HTML PDF generation (no authentication required)"""
    try:
        print(f"🐛 Debug HTML PDF generation - Content length: {len(resume_content)}")
        
        # Process resume content into structured data
        processor = ResumeProcessor()
        structured_data = processor.process_resume_content(resume_content, {})
        print(f"✅ Resume processed: {len(structured_data)} data fields")
        
        # Render HTML template
        template_path = os.path.join(os.path.dirname(__file__), "resume_template.html")
        if not os.path.exists(template_path):
            return {"error": f"Template file not found: {template_path}"}
        
        html_content = template_engine.render_template_file(template_path, structured_data)
        print(f"✅ HTML generated: {len(html_content)} characters")
        
        # Generate PDF using Playwright
        pdf_bytes = await html_pdf_generator.generate_pdf_from_html(html_content, "debug_user")
        
        if not pdf_bytes:
            return {"error": "PDF generation failed - no bytes returned"}
        
        print(f"✅ PDF generated: {len(pdf_bytes)} bytes")
        
        # Return PDF as base64 for debugging
        import base64
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        return {
            "success": True,
            "pdf_size": len(pdf_bytes),
            "pdf_base64": pdf_base64[:100] + "..." if len(pdf_base64) > 100 else pdf_base64,
            "message": "PDF generated successfully"
        }
        
    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"Debug error: {str(e)}"}

@app.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get user's saved profile"""
    if not os.getenv("DATABASE_URL"):
        raise HTTPException(status_code=503, detail="Database not configured")
    
    user_id = current_user["id"]
    profile = await db_manager.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.post("/profile")
async def upsert_profile(
    profile_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Save or update user profile"""
    if not os.getenv("DATABASE_URL"):
        raise HTTPException(status_code=503, detail="Database not configured")
    
    user_id = current_user["id"]
    role_family = profile_data.get("meta", {}).get("role_family")
    
    await db_manager.upsert_profile(user_id, profile_data, role_family)
    return {"status": "ok", "message": "Profile saved successfully"}

@app.post("/generate-resume/")
async def generate_resume(
    job_offer_url: str = Form(...),
    profile_json: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Generate resume from profile JSON and job offer URL"""
    user_id = current_user["id"]
    
    # Read and validate profile data
    profile_data = await profile_json.read()
    profile_str = profile_data.decode("utf-8")
    
    try:
        # Validate JSON
        profile_dict = json.loads(profile_str)
        
        # Save profile to database (if configured)
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            try:
                role_family = profile_dict.get("meta", {}).get("role_family")
                await db_manager.upsert_profile(user_id, profile_dict, role_family)
                print("✅ Profile saved to database")
            except Exception as e:
                print(f"⚠️  Failed to save profile to database: {e}")
        
        # Generate resume using AI agent
        resume = await run_agent(profile_str, job_offer_url)
        
        if not resume:
            raise HTTPException(status_code=500, detail="Failed to generate resume")
        
        # Generate unique resume ID
        resume_id = str(uuid.uuid4())
        
        # Save resume metadata (if database configured)
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            try:
                await db_manager.save_resume_metadata(user_id, resume_id, job_offer_url)
                print("✅ Resume metadata saved")
            except Exception as e:
                print(f"⚠️  Failed to save resume metadata: {e}")
        
        return {
            "resume": resume,
            "resume_id": resume_id,
            "user_id": user_id
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")

@app.post("/generate-pdf/")
async def generate_pdf(
    resume_content: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """Generate PDF from resume content"""
    user_id = current_user["id"]
    
    try:
        # Generate PDF
        pdf_generator = ResumePDFGenerator()
        pdf_bytes = pdf_generator.generate_pdf(resume_content, user_id)
        
        # Create streaming response
        pdf_stream = io.BytesIO(pdf_bytes)
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=resume_{user_id}.pdf"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

@app.post("/generate-and-store-pdf/")
async def generate_and_store_pdf(
    resume_content: str = Form(...),
    resume_id: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """Generate PDF from resume content and store in Supabase Storage"""
    user_id = current_user["id"]
    
    try:
        # Generate PDF
        pdf_generator = ResumePDFGenerator()
        pdf_bytes = pdf_generator.generate_pdf(resume_content, user_id)
        
        # Store PDF in Supabase Storage
        storage_url = await storage_manager.upload_pdf(pdf_bytes, user_id, resume_id)
        
        if storage_url:
            # Update resume metadata with storage URL
            if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
                try:
                    await db_manager.update_resume_storage_url(user_id, resume_id, storage_url)
                    print("✅ Resume storage URL updated in database")
                except Exception as e:
                    print(f"⚠️  Failed to update storage URL in database: {e}")
            
            return {
                "status": "success",
                "message": "PDF generated and stored successfully",
                "storage_url": storage_url,
                "resume_id": resume_id
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to store PDF in storage")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating and storing PDF: {str(e)}")

@app.post("/generate-html-pdf/")
async def generate_html_pdf(
    resume_content: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """Generate PDF from resume content using Playwright HTML rendering"""
    user_id = current_user["id"]
    
    try:
        print(f"🚀 Starting HTML PDF generation for user: {user_id}")
        print(f"📄 Resume content length: {len(resume_content)} characters")
        
        # Get user profile for better data extraction
        profile_data = {}
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            try:
                print("🔍 Fetching user profile...")
                profile = await db_manager.get_profile(user_id)
                if profile:
                    profile_data = profile.get("profile", {})
                    print(f"✅ Profile data retrieved: {len(str(profile_data))} characters")
                else:
                    print("⚠️  No profile data found")
            except Exception as e:
                print(f"⚠️  Failed to get profile data: {e}")
        
        # Process resume content into structured data
        print("🔄 Processing resume content...")
        processor = ResumeProcessor()
        structured_data = processor.process_resume_content(resume_content, profile_data)
        print(f"✅ Resume processed: {len(structured_data)} data fields")
        
        # Render HTML template
        print("🎨 Rendering HTML template...")
        template_path = os.path.join(os.path.dirname(__file__), "resume_template.html")
        if not os.path.exists(template_path):
            raise HTTPException(status_code=500, detail=f"Template file not found: {template_path}")
        
        html_content = template_engine.render_template_file(template_path, structured_data)
        print(f"✅ HTML generated: {len(html_content)} characters")
        
        # Generate PDF using Playwright
        print("📄 Generating PDF with Playwright...")
        pdf_bytes = await html_pdf_generator.generate_pdf_from_html(html_content, user_id)
        
        if not pdf_bytes:
            raise HTTPException(status_code=500, detail="PDF generation failed - no bytes returned")
        
        print(f"✅ PDF generated: {len(pdf_bytes)} bytes")
        
        # Create streaming response
        print("📤 Creating streaming response...")
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=resume_{user_id}.pdf"}
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"❌ Error generating HTML PDF: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating HTML PDF: {str(e)}")

@app.post("/generate-and-store-html-pdf/")
async def generate_and_store_html_pdf(
    resume_content: str = Form(...),
    resume_id: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """Generate PDF from resume content using Playwright and store in Supabase Storage"""
    user_id = current_user["id"]
    
    try:
        # Get user profile for better data extraction
        profile_data = {}
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            try:
                profile = await db_manager.get_profile(user_id)
                if profile:
                    profile_data = profile.get("profile", {})
            except Exception as e:
                print(f"⚠️  Failed to get profile data: {e}")
        
        # Process resume content into structured data
        processor = ResumeProcessor()
        structured_data = processor.process_resume_content(resume_content, profile_data)
        
        # Render HTML template
        template_path = "resume_template.html"
        html_content = template_engine.render_template_file(template_path, structured_data)
        
        # Generate PDF using Playwright
        pdf_bytes = await html_pdf_generator.generate_pdf_from_html(html_content, user_id)
        
        # Store PDF in Supabase Storage
        storage_url = await storage_manager.upload_pdf(pdf_bytes, user_id, resume_id)
        
        if storage_url:
            # Update resume metadata with storage URL
            if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
                try:
                    await db_manager.update_resume_storage_url(user_id, resume_id, storage_url)
                    print("✅ Resume storage URL updated in database")
                except Exception as e:
                    print(f"⚠️  Failed to update storage URL in database: {e}")
            
            return {
                "status": "success",
                "message": "HTML PDF generated and stored successfully",
                "storage_url": storage_url,
                "resume_id": resume_id
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to store PDF in storage")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating and storing HTML PDF: {str(e)}")

@app.get("/user-resumes/")
async def get_user_resumes(current_user: dict = Depends(get_current_user)):
    """Get list of user's stored resumes"""
    user_id = current_user["id"]
    
    try:
        # Get resume metadata from database
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            async with await db_manager.get_connection() as conn:
                rows = await conn.fetch(
                    "SELECT resume_id, job_url, status, created_at, storage_url FROM resume_metadata WHERE user_id = $1 ORDER BY created_at DESC",
                    user_id
                )
                resumes = [dict(row) for row in rows]
                return {"resumes": resumes}
        else:
            return {"resumes": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user resumes: {str(e)}")

@app.delete("/resume/{resume_id}/")
async def delete_resume(resume_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a resume and its PDF from storage"""
    user_id = current_user["id"]
    
    try:
        # Delete PDF from storage
        storage_deleted = await storage_manager.delete_pdf(user_id, resume_id)
        
        # Delete metadata from database
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
            async with await db_manager.get_connection() as conn:
                await conn.execute(
                    "DELETE FROM resume_metadata WHERE user_id = $1 AND resume_id = $2",
                    user_id, resume_id
                )
        
        return {
            "status": "success",
            "message": "Resume deleted successfully",
            "storage_deleted": storage_deleted
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting resume: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "cv-builder-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
