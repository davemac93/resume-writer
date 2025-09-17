import asyncio
from lib.agent import run_agent

with open("dawid_maciejewski_profile.json", "r", encoding="utf-8") as f:
    profile_json = f.read()

job_offer_url = "https://example.com/job-offer"

result = asyncio.run(run_agent(profile_json, job_offer_url))
print(result)