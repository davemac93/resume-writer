from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from lib.agent import run_agent
import asyncio
import json

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-resume/")
async def generate_resume(
    job_offer_url: str = Form(...),
    profile_json: UploadFile = File(...)
):
    profile_data = await profile_json.read()
    profile_str = profile_data.decode("utf-8")
    resume = await run_agent(profile_str, job_offer_url)
    return {"resume": resume}

async def main():
    await run_agent()

if __name__ == "__main__":
    asyncio.run(main())
