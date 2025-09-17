from dotenv import load_dotenv
load_dotenv()

import asyncio
from lib.agent import run_agent

async def main():
    await run_agent()

if __name__ == "__main__":
    asyncio.run(main())
