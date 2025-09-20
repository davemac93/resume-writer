#!/usr/bin/env python3
"""
Migration script to move existing JSON profiles into the database
"""
import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db_manager

async def migrate_json_profiles():
    """Migrate JSON profile files to database"""
    print("🚀 Starting JSON profile migration...")
    
    # Check if database is configured
    if not os.getenv("DATABASE_URL"):
        print("❌ DATABASE_URL not configured. Please set up your .env file.")
        return
    
    try:
        # Initialize database connection
        await db_manager.init_pool()
        print("✅ Database connection established")
        
        # Find JSON profile files
        backend_dir = Path(__file__).parent
        json_files = list(backend_dir.glob("*.json"))
        
        if not json_files:
            print("⚠️  No JSON profile files found in backend directory")
            return
        
        print(f"📁 Found {len(json_files)} JSON files to migrate")
        
        migrated_count = 0
        error_count = 0
        
        for json_file in json_files:
            try:
                print(f"\n📄 Processing {json_file.name}...")
                
                # Read JSON file
                with open(json_file, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                
                # Extract user info (use filename as user_id for migration)
                user_id = json_file.stem  # filename without extension
                
                # Extract role family from meta if available
                role_family = profile_data.get("meta", {}).get("role_family", "unknown")
                
                # Save to database
                await db_manager.upsert_profile(user_id, profile_data, role_family)
                
                print(f"✅ Migrated profile for user: {user_id}")
                migrated_count += 1
                
            except Exception as e:
                print(f"❌ Error migrating {json_file.name}: {e}")
                error_count += 1
        
        print(f"\n📊 Migration Summary:")
        print(f"   ✅ Successfully migrated: {migrated_count} profiles")
        print(f"   ❌ Errors: {error_count} profiles")
        
        if migrated_count > 0:
            print(f"\n🎉 Migration completed! {migrated_count} profiles are now in the database.")
            print("   You can now use the web interface to manage these profiles.")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
    finally:
        # Close database connection
        await db_manager.close_pool()
        print("✅ Database connection closed")

async def list_migrated_profiles():
    """List all profiles in the database"""
    print("📋 Listing all profiles in database...")
    
    try:
        await db_manager.init_pool()
        
        async with await db_manager.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT user_id, role_family, created_at, updated_at 
                FROM profiles 
                ORDER BY created_at DESC
            """)
            
            if rows:
                print(f"\n📊 Found {len(rows)} profiles in database:")
                print("-" * 80)
                for row in rows:
                    print(f"User ID: {row['user_id']}")
                    print(f"Role Family: {row['role_family']}")
                    print(f"Created: {row['created_at']}")
                    print(f"Updated: {row['updated_at']}")
                    print("-" * 80)
            else:
                print("📭 No profiles found in database")
                
    except Exception as e:
        print(f"❌ Error listing profiles: {e}")
    finally:
        await db_manager.close_pool()

async def main():
    """Main migration function"""
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        await list_migrated_profiles()
    else:
        await migrate_json_profiles()

if __name__ == "__main__":
    asyncio.run(main())
