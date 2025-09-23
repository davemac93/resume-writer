import os
import httpx
from fastapi import HTTPException, Depends, Header
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
        print(f"❌ Auth failed with status {resp.status_code}: {resp.text}")
        raise HTTPException(status_code=401, detail=f"Invalid token (status: {resp.status_code})")
    
    user_data = resp.json()
    print(f"✅ Auth successful for user: {user_data.get('id', 'unknown')}")
    return user_data

async def get_current_user(authorization: str = Header(None)) -> Dict[str, Any]:
    """Get current user from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = authorization.split(" ")[1]
    print(f"🔑 Received token: {token[:20]}..." if token else "No token")
    user_data = await get_user_from_token(token)
    
    # Extract user ID from the response
    user_id = user_data.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user data")
    
    return {"id": user_id, "sub": user_id}
