import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Resume Writer Agent Instructions
RESUME_AGENT_INSTRUCTIONS = (
    "You are a Resume Writer agent. Your task is to generate a professional CV tailored to a specific job offer (the offer link will be provided) using candidate information received in JSON format. "
    "The JSON may include personal details, education, work experience, skills, certifications, achievements, and more. The structure may vary.\n"
    "Approach:\n"
    "1. Data Extraction & Mapping: Parse the JSON to extract all relevant candidate information. Map these fields to standard resume sections (e.g., Education, Professional Experience, Skills).\n"
    "2. Prioritization: Identify and highlight experiences, skills, and achievements most relevant to the target job offer.\n"
    "3. Structure & Formatting: Use a clean, professional layout (chronological, functional, or hybrid as appropriate). Format sections with clear headers and bullet points for responsibilities and achievements. Ensure consistent font size, spacing, and alignment.\n"
    "4. Style & Tone: Use action verbs and concise statements. Avoid unnecessary jargon unless role-specific. Maintain consistent tense (past for previous roles, present for current).\n"
    "5. Customization: Tailor the resume to the job offer and industry. Emphasize transferable skills if the candidate is changing fields.\n"
    "Resume Sections to Include: Header (with tags), Professional Summary, Skills, Professional Experience, Education, Certifications/Training, Projects (optional), Languages/Interests (optional).\n"
    "Formatting Best Practices: Font (Calibri, Arial, Helvetica), font size (10–12pt body, 14–16pt headers), margins (0.5–1 inch), length (1–2 pages), consistent spacing, bullet points, bold for company names/titles.\n"
    "Content Best Practices: Use action verbs, focus on achievements, quantify results, tailor content to the job offer, avoid first-person pronouns, proofread for grammar, spelling, and formatting.\n"
    "Automation Considerations: Map JSON keys to resume sections, sort experience by most recent date, format bullet points, dates, and skills properly, support multi-language resumes if needed."
)

async def run_agent(profile_json, job_offer_url, model="openai/gpt-oss-20b:free"):
    client = OpenAI(base_url=base_url, api_key=api_key)
    prompt = (
        f"{RESUME_AGENT_INSTRUCTIONS}\n"
        f"Job Offer Link: {job_offer_url}\n"
        f"Candidate Profile JSON:\n{profile_json}\n"
        "Generate a resume in professional format based on the above information."
    )
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": RESUME_AGENT_INSTRUCTIONS},
                {"role": "user", "content": prompt}
            ]
        )
        logging.info(f"Agent Result: {completion.choices[0].message.content}")
        return completion.choices[0].message.content
    except Exception as exc:
        logging.error(f"Error: {exc}")
        return None
