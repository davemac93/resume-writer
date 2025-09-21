#!/usr/bin/env python3
"""
Check files in Supabase storage bucket
"""
import asyncio
from storage import storage_manager

async def check_storage_files():
    print("🔍 Checking files in Supabase storage...")
    
    try:
        result = storage_manager.client.storage.from_("resumes").list()
        print(f"📁 Files in bucket: {len(result) if result else 0}")
        
        if result:
            for file in result:
                print(f"  - {file['name']} ({file.get('size', 'unknown')} bytes)")
        else:
            print("  No files found")
            
    except Exception as e:
        print(f"❌ Error checking storage: {e}")

if __name__ == "__main__":
    asyncio.run(check_storage_files())
