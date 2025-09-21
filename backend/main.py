from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from lib.agent import run_agent
from auth import get_current_user
from database_supabase_api import supabase_db_manager as db_manager
from html_pdf_generator import html_pdf_generator, cleanup_playwright
from flexible_resume_processor import FlexibleResumeProcessor
from manual_template_processor import process_template_manually
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
        print("✅ Supabase configured")
    else:
        print("⚠️  Supabase not configured - some features will be disabled")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down CV Builder API...")
    await cleanup_playwright()

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
        structured_data = processor.process_resume_content(markdown_content, {})
        
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
        
        html_content = process_template_manually(template_content, structured_data)
        
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
