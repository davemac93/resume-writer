import os
import uuid
from supabase import create_client, Client
from typing import Optional
import logging

class SupabaseStorageManager:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.bucket_name = os.getenv("SUPABASE_STORAGE_BUCKET", "resumes")
        self.client: Optional[Client] = None
        
        if self.supabase_url and self.supabase_service_key:
            self.client = create_client(self.supabase_url, self.supabase_service_key)
            logging.info("Supabase Storage client initialized")
        else:
            logging.warning("Supabase Storage not configured - missing environment variables")

    async def upload_pdf(self, pdf_bytes: bytes, user_id: str, resume_id: str) -> Optional[str]:
        """Upload PDF to Supabase Storage and return the public URL"""
        if not self.client:
            logging.error("Supabase Storage client not initialized")
            return None
        
        try:
            # Create file path: user_id/resume_id.pdf
            file_path = f"{user_id}/{resume_id}.pdf"
            
            # Upload file to storage
            result = self.client.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=pdf_bytes,
                file_options={"content-type": "application/pdf"}
            )
            
            if result:
                # Get public URL
                public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
                logging.info(f"PDF uploaded successfully: {public_url}")
                return public_url
            else:
                logging.error("Failed to upload PDF to storage")
                return None
                
        except Exception as e:
            logging.error(f"Error uploading PDF to storage: {str(e)}")
            return None

    async def delete_pdf(self, user_id: str, resume_id: str) -> bool:
        """Delete PDF from Supabase Storage"""
        if not self.client:
            logging.error("Supabase Storage client not initialized")
            return False
        
        try:
            file_path = f"{user_id}/{resume_id}.pdf"
            result = self.client.storage.from_(self.bucket_name).remove([file_path])
            logging.info(f"PDF deleted successfully: {file_path}")
            return True
        except Exception as e:
            logging.error(f"Error deleting PDF from storage: {str(e)}")
            return False

    async def list_user_pdfs(self, user_id: str) -> list:
        """List all PDFs for a user"""
        if not self.client:
            logging.error("Supabase Storage client not initialized")
            return []
        
        try:
            result = self.client.storage.from_(self.bucket_name).list(path=user_id)
            return result or []
        except Exception as e:
            logging.error(f"Error listing user PDFs: {str(e)}")
            return []

# Global storage manager instance
storage_manager = SupabaseStorageManager()
