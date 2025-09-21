#!/usr/bin/env python3
"""
Test Supabase storage connection and bucket access
"""
import asyncio
import os
from dotenv import load_dotenv
from storage import storage_manager

async def test_storage_connection():
    print("🔍 Testing Supabase storage connection...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if storage manager is initialized
    if not storage_manager.client:
        print("❌ Storage client not initialized")
        return False
    
    print("✅ Storage client initialized")
    
    # Test bucket access by trying to list files
    try:
        # Try to list files in the bucket (this will fail if bucket doesn't exist)
        result = storage_manager.client.storage.from_("resumes").list()
        print("✅ Bucket 'resumes' is accessible")
        print(f"📁 Files in bucket: {len(result) if result else 0}")
        return True
    except Exception as e:
        print(f"❌ Error accessing bucket: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_storage_connection())
