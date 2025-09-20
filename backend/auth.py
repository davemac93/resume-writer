import os
import httpx
from fastapi import HTTPException
from typing import Dict, Any

SUPABASE_URL = os.getenv("SUPABASE_URL")  # e.g. https://xyz.supabase.co

async def get_user_from_token(token: str) -> Dict[str, Any]:
    """Return user dict or raise HTTPException(401)."""
    if not SUPABASE_URL:
        raise HTTPException(status_code=503, detail="Authentication not configured. Please set SUPABASE_URL environment variable.")
    
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{SUPABASE_URL}/auth/v1/user",
                headers={
                    "Authorization": f"Bearer {token}",
                    "apikey": os.getenv("SUPABASE_ANON_KEY", "")
                }
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=401, detail=f"Auth service error: {str(e)}")
    
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_data = resp.json()
    return user_data
