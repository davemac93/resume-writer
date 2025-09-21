#!/usr/bin/env python3
"""
CV Generation API - RESTful API for generating CVs from markdown content
"""
import os
import sys
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

sys.path.append(os.path.dirname(__file__))

from manual_template_processor import process_template_manually
from resume_processor import ResumeProcessor
from html_pdf_generator import HTMLToPDFGenerator

app = FastAPI(title="CV Generator API", version="1.0.0")

class CVRequest(BaseModel):
    markdown_content: str
    user_id: Optional[str] = None
    filename: Optional[str] = None

class CVResponse(BaseModel):
    success: bool
    message: str
    pdf_filename: Optional[str] = None
    html_filename: Optional[str] = None
    file_size: Optional[int] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "CV Generator API is running", "version": "1.0.0"}

@app.post("/generate-cv", response_model=CVResponse)
async def generate_cv(request: CVRequest):
    """
    Generate CV from markdown content
    
    Args:
        request: CVRequest containing markdown content and optional parameters
        
    Returns:
        CVResponse with generation results
    """
    
    try:
        # Generate unique user ID if not provided
        user_id = request.user_id or str(uuid.uuid4())
        
        # Generate filename if not provided
        if request.filename:
            pdf_filename = request.filename if request.filename.endswith('.pdf') else f"{request.filename}.pdf"
        else:
            pdf_filename = f"cv_{user_id}.pdf"
        
        html_filename = pdf_filename.replace('.pdf', '.html')
        
        print(f"🎯 Generating CV for user: {user_id}")
        print(f"📄 Resume content length: {len(request.markdown_content)} characters")
        
        # Process resume content
        processor = ResumeProcessor()
        structured_data = processor.process_resume_content(request.markdown_content, {})
        
        print(f"✅ Processed data keys: {list(structured_data.keys())}")
        print(f"📊 Experience entries: {len(structured_data.get('experience', []))}")
        print(f"🏷️  Tags: {len(structured_data.get('tags', []))}")
        print(f"🎓 Education entries: {len(structured_data.get('education', []))}")
        print(f"📜 Certifications: {len(structured_data.get('certifications', []))}")
        print(f"🚀 Projects: {len(structured_data.get('projects', []))}")
        
        # Test template rendering
        template_path = os.path.join(os.path.dirname(__file__), "resume_template.html")
        
        if not os.path.exists(template_path):
            raise HTTPException(status_code=500, detail="Template file not found")
        
        print("🎨 Rendering template...")
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        html_content = process_template_manually(template_content, structured_data)
        
        # Check if template syntax is still present
        if "{{" in html_content and "}}" in html_content:
            print("❌ Template syntax still present in rendered HTML!")
            raise HTTPException(status_code=500, detail="Template processing failed - syntax errors detected")
        
        print("✅ Template syntax successfully processed!")
        
        # Generate PDF using Playwright
        print("📄 Generating PDF with Playwright...")
        pdf_generator = HTMLToPDFGenerator()
        
        try:
            pdf_bytes = await pdf_generator.generate_pdf_from_html(html_content, user_id)
            
            if pdf_bytes:
                print(f"✅ PDF generated successfully: {len(pdf_bytes)} bytes")
                
                # Save the PDF
                with open(pdf_filename, "wb") as f:
                    f.write(pdf_bytes)
                print(f"💾 CV PDF saved as: {pdf_filename}")
                
                # Also save the HTML for inspection
                with open(html_filename, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"💾 HTML version saved as: {html_filename}")
                
                return CVResponse(
                    success=True,
                    message="CV generated successfully",
                    pdf_filename=pdf_filename,
                    html_filename=html_filename,
                    file_size=len(pdf_bytes)
                )
            else:
                raise HTTPException(status_code=500, detail="PDF generation failed - no bytes returned")
                
        except Exception as e:
            print(f"❌ PDF generation error: {e}")
            raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
        finally:
            await pdf_generator.close()
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "CV Generator API is running"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting CV Generator API...")
    print("📖 API Documentation available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
