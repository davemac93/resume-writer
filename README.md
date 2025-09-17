# Resume Writer Agent

Generate professional, tailored resumes from candidate profile JSON and job offer links using OpenRouter AI.

## Overview
This project is an automated Resume Writer agent that leverages OpenRouter's AI models to create high-quality CVs. It parses candidate information from a JSON file and customizes the resume for a specific job offer, following best practices in resume writing and formatting.

## Features
- Parses candidate profile JSON (flexible structure)
- Maps data to standard resume sections
- Prioritizes relevant experience and skills for the target job
- Follows professional resume formatting and style guidelines
- Customizes output for specific job offers
- Uses OpenRouter AI via the OpenAI SDK

## How It Works
1. **Data Extraction & Mapping:**
   - Extracts personal info, education, work experience, skills, certifications, achievements, and more from JSON.
   - Maps fields to resume sections (e.g., Education, Professional Experience).
2. **Prioritization:**
   - Highlights achievements and skills most relevant to the job offer.
3. **Structure & Formatting:**
   - Generates a clean, professional resume (chronological, functional, or hybrid).
   - Uses bullet points, clear headers, and consistent formatting.
4. **Customization:**
   - Tailors resume for the job offer and industry.
   - Emphasizes transferable skills if needed.

## Usage
1. Place your candidate profile JSON in the project directory (see example: `dawid_maciejewski_profile.json`).
2. Set your OpenRouter API key and base URL in a `.env` file:
   ```
   OPENROUTER_API_KEY=your-api-key-here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```
3. Run the agent with your JSON and job offer link:
   ```python
   import json
   from lib.agent import run_agent
   
   with open('dawid_maciejewski_profile.json') as f:
       profile_json = f.read()
   job_offer_url = "https://example.com/job-offer"
   
   # If using asyncio
   import asyncio
   result = asyncio.run(run_agent(profile_json, job_offer_url))
   print(result)
   ```

## Resume Generation Guide
- Chronological, functional, or hybrid formats supported
- Recommended sections: Header, Professional Summary, Skills, Experience, Education, Certifications, Projects, Languages/Interests
- Professional style: clean fonts, consistent formatting, action verbs, quantified achievements
- Content tailored to job offer and candidate background

## Example Candidate Profile JSON
See `dawid_maciejewski_profile.json` for a sample structure.

## Requirements
- Python 3.10+
- `openai`, `python-dotenv`

## Installation
```bash
pip install -r requirements.txt
```

## License
MIT

## Author
Dawid Maciejewski
