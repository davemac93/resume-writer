from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from lib.agent import run_agent
import json
import uuid

app = FastAPI(title="CV Builder API - Simple Mode", version="1.0.0")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "CV Builder API - Simple Mode", 
        "version": "1.0.0",
        "note": "Running without authentication and database"
    }

@app.post("/generate-resume/")
async def generate_resume(
    job_offer_url: str = Form(...),
    profile_json: UploadFile = File(...)
):
    """Generate resume from profile JSON and job offer URL (no auth required)"""
    
    # Read and validate profile data
    profile_data = await profile_json.read()
    profile_str = profile_data.decode("utf-8")
    
    try:
        # Validate JSON
        profile_dict = json.loads(profile_str)
        
        # Generate resume using AI agent
        resume = await run_agent(profile_str, job_offer_url)
        
        if not resume:
            raise HTTPException(status_code=500, detail="Failed to generate resume")
        
        # Generate unique resume ID
        resume_id = str(uuid.uuid4())
        
        return {
            "resume": resume,
            "resume_id": resume_id,
            "message": "Resume generated successfully (simple mode)"
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "cv-builder-api-simple"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
