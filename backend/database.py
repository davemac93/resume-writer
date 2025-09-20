import os
import asyncpg
import json
from typing import Dict, Any, Optional
import logging

DATABASE_URL = os.getenv("DATABASE_URL")

class DatabaseManager:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def init_pool(self):
        """Initialize connection pool"""
        if not self.pool:
            self.pool = await asyncpg.create_pool(DATABASE_URL)
            logging.info("Database pool initialized")

    async def close_pool(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            logging.info("Database pool closed")

    async def get_connection(self):
        """Get database connection from pool"""
        if not self.pool:
            await self.init_pool()
        return self.pool.acquire()

    async def upsert_profile(self, user_id: str, profile_data: Dict[str, Any], role_family: str = None):
        """Insert or update user profile"""
        async with await self.get_connection() as conn:
            await conn.execute("""
                INSERT INTO profiles (user_id, profile, role_family, updated_at)
                VALUES ($1, $2::jsonb, $3, now())
                ON CONFLICT (user_id) DO UPDATE SET 
                    profile = $2::jsonb, 
                    role_family = $3, 
                    updated_at = now()
            """, user_id, json.dumps(profile_data), role_family)

    async def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile"""
        async with await self.get_connection() as conn:
            row = await conn.fetchrow(
                "SELECT profile, role_family, created_at, updated_at FROM profiles WHERE user_id = $1",
                user_id
            )
            if row:
                return {
                    "profile": row["profile"],
                    "role_family": row["role_family"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                }
            return None

    async def save_resume_metadata(self, user_id: str, resume_id: str, job_url: str, status: str = "generated"):
        """Save resume generation metadata"""
        async with await self.get_connection() as conn:
            await conn.execute("""
                INSERT INTO resume_metadata (user_id, resume_id, job_url, status, created_at)
                VALUES ($1, $2, $3, $4, now())
            """, user_id, resume_id, job_url, status)

    async def update_resume_storage_url(self, user_id: str, resume_id: str, storage_url: str):
        """Update resume metadata with storage URL"""
        async with await self.get_connection() as conn:
            await conn.execute("""
                UPDATE resume_metadata 
                SET storage_url = $1 
                WHERE user_id = $2 AND resume_id = $3
            """, storage_url, user_id, resume_id)

# Global database manager instance
db_manager = DatabaseManager()
