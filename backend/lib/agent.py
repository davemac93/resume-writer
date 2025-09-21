import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Resume Writer Agent Instructions - Generate Markdown
RESUME_AGENT_INSTRUCTIONS = (
    "You are a Resume Writer agent. Your task is to generate a professional CV in MARKDOWN format tailored to a specific job offer using candidate information received in JSON format. "
    "The JSON may include personal details, education, work experience, skills, certifications, achievements, and more. The structure may vary.\n\n"
    
    "IMPORTANT: You MUST generate the output in the EXACT markdown format specified below. Follow this template precisely:\n\n"
    
    "```markdown\n"
    "**FULL NAME**\n"
    "Job Title | Key Skills (3-4 skills) | Location\n"
    "City, Country | Phone | Email | [LinkedIn](URL) | [GitHub](URL)\n\n"
    "---\n\n"
    "### Professional Summary\n"
    "[2-3 sentences describing the candidate's experience, key achievements, and value proposition]\n\n"
    "---\n\n"
    "### Key Competencies\n\n"
    "| Technical | Process & Project | Soft & Leadership |\n"
    "|-----------|------------------|--------------------|\n"
    "| [Technical skills separated by commas] | [Process skills separated by commas] | [Soft skills separated by commas] |\n\n"
    "---\n\n"
    "### Professional Experience\n\n"
    "**Job Title**\n"
    "**Company Name, Location** | Start Date – End Date\n"
    "- [Achievement 1 with quantified results]\n"
    "- [Achievement 2 with quantified results]\n"
    "- [Achievement 3 with quantified results]\n\n"
    "**Job Title**\n"
    "**Company Name, Location** | Start Date – End Date\n"
    "- [Achievement 1 with quantified results]\n"
    "- [Achievement 2 with quantified results]\n\n"
    "---\n\n"
    "### Education\n\n"
    "**Degree Name** – Institution Name | Start Date – End Date\n\n"
    "---\n\n"
    "### Languages\n\n"
    "- **Language 1** – Proficiency Level\n"
    "- **Language 2** – Proficiency Level\n\n"
    "---\n\n"
    "### [Optional Sections - Only include if relevant]\n\n"
    "### Certifications & Training\n"
    "- **Certification Name** – Provider (Year)\n"
    "- **Certification Name** – Provider (Year)\n\n"
    "### Selected Projects\n"
    "| Project | Tools | Impact |\n"
    "|---------|-------|--------|\n"
    "| **Project Name** | Tools used | Brief impact description |\n"
    "| **Project Name** | Tools used | Brief impact description |\n\n"
    "### Core Technical Skills\n"
    "- **Category 1:** skill1, skill2, skill3\n"
    "- **Category 2:** skill1, skill2, skill3\n\n"
    "### Interests\n"
    "- Interest 1\n"
    "- Interest 2\n"
    "- Interest 3\n\n"
    "### Additional Information\n"
    "- Any other relevant information\n\n"
    "---\n"
    "```\n\n"
    
    "RULES:\n"
    "1. ALWAYS include these sections: Name and contact details, Professional Summary, Professional Experience, Education, Languages\n"
    "2. ONLY include optional sections if they have content: Certifications & Training, Selected Projects, Core Technical Skills, Interests, Additional Information\n"
    "3. Use **bold** for job titles, company names, degree names\n"
    "4. Use *italic* for locations, dates\n"
    "5. Use bullet points (-) for lists\n"
    "6. Use tables for structured data\n"
    "7. Use [LinkedIn](URL) format for links\n"
    "8. Quantify achievements with numbers and percentages\n"
    "9. Use action verbs (Led, Developed, Implemented, etc.)\n"
    "10. Keep descriptions concise but impactful\n"
    "11. Use 'MMM YYYY – MMM YYYY' or 'MMM YYYY – Present' date format\n"
    "12. Tailor content to the target role and job offer\n\n"
    
    "Your response should ONLY contain the markdown-formatted resume, nothing else."
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
