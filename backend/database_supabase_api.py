"""
Database manager using Supabase API instead of direct PostgreSQL connection
This is an alternative to the direct PostgreSQL approach
"""
import os
import json
from typing import Dict, Any, Optional, List
from supabase import create_client, Client
import logging

class SupabaseDatabaseManager:
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if self.supabase_url and self.supabase_service_key:
            try:
                self.supabase = create_client(self.supabase_url, self.supabase_service_key)
                logging.info("Supabase API client initialized")
            except Exception as e:
                logging.error(f"Failed to initialize Supabase API client: {e}")
        else:
            logging.warning("Supabase URL or Service Role Key not set. Database features will be disabled.")

    async def init_pool(self):
        """Initialize connection (no-op for API client)"""
        if not self.supabase:
            raise Exception("Supabase client not initialized")
        logging.info("Supabase API client ready")

    async def close_pool(self):
        """Close connection (no-op for API client)"""
        logging.info("Supabase API client closed")

    async def get_connection(self):
        """Get connection context (no-op for API client)"""
        if not self.supabase:
            raise Exception("Supabase client not initialized")
        return self

    async def upsert_profile(self, user_id: str, profile_data: Dict[str, Any], role_family: str = None):
        """Insert or update user profile using Supabase API"""
        if not self.supabase:
            raise Exception("Supabase client not initialized")
        
        try:
            # Check if profile exists
            existing = self.supabase.table('profiles').select('id').eq('user_id', user_id).execute()
            
            profile_record = {
                'user_id': user_id,
                'profile': profile_data,
                'role_family': role_family
            }
            
            if existing.data:
                # Update existing profile
                result = self.supabase.table('profiles').update(profile_record).eq('user_id', user_id).execute()
                logging.info(f"Profile updated for user {user_id}")
            else:
                # Insert new profile
                result = self.supabase.table('profiles').insert(profile_record).execute()
                logging.info(f"Profile created for user {user_id}")
            
            return result.data
        except Exception as e:
            logging.error(f"Error upserting profile: {e}")
            raise e

    async def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile using Supabase API"""
        if not self.supabase:
            raise Exception("Supabase client not initialized")
        
        try:
            result = self.supabase.table('profiles').select('*').eq('user_id', user_id).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logging.error(f"Error getting profile: {e}")
            return None

    async def save_resume_metadata(self, user_id: str, resume_id: str, job_url: str = None):
        """Save resume metadata using Supabase API"""
        if not self.supabase:
            raise Exception("Supabase client not initialized")
        
        try:
            metadata_record = {
                'user_id': user_id,
                'resume_id': resume_id,
                'job_url': job_url,
                'status': 'generated'
            }
            
            result = self.supabase.table('resume_metadata').insert(metadata_record).execute()
            logging.info(f"Resume metadata saved for user {user_id}")
            return result.data
        except Exception as e:
            logging.error(f"Error saving resume metadata: {e}")
            raise e

    async def update_resume_storage_url(self, user_id: str, resume_id: str, storage_url: str):
        """Update resume metadata with storage URL using Supabase API"""
        if not self.supabase:
            raise Exception("Supabase client not initialized")
        
        try:
            result = self.supabase.table('resume_metadata').update({
                'storage_url': storage_url
            }).eq('user_id', user_id).eq('resume_id', resume_id).execute()
            
            logging.info(f"Resume storage URL updated for user {user_id}")
            return result.data
        except Exception as e:
            logging.error(f"Error updating resume storage URL: {e}")
            raise e

    async def get_user_resumes(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's resumes using Supabase API"""
        if not self.supabase:
            raise Exception("Supabase client not initialized")
        
        try:
            result = self.supabase.table('resume_metadata').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            return result.data or []
        except Exception as e:
            logging.error(f"Error getting user resumes: {e}")
            return []

    async def delete_resume(self, user_id: str, resume_id: str) -> bool:
        """Delete resume metadata using Supabase API"""
        if not self.supabase:
            raise Exception("Supabase client not initialized")
        
        try:
            result = self.supabase.table('resume_metadata').delete().eq('user_id', user_id).eq('resume_id', resume_id).execute()
            logging.info(f"Resume deleted for user {user_id}")
            return True
        except Exception as e:
            logging.error(f"Error deleting resume: {e}")
            return False

# Global instance
supabase_db_manager = SupabaseDatabaseManager()
