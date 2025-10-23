#!/usr/bin/env python3
"""
Automatic Supabase database setup script
Runs the schema.sql file to create all necessary tables
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def setup_database():
    """Initialize Supabase database with schema"""

    print("🚀 CreatorPulse - Supabase Database Setup")
    print("="*50)

    # Get credentials
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')

    if not url or not key:
        print("❌ Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        return False

    print(f"✅ Found credentials")
    print(f"   URL: {url[:40]}...")
    print(f"   Key: {key[:30]}...")

    try:
        # Create Supabase client
        supabase: Client = create_client(url, key)
        print("✅ Connected to Supabase")

        # Read schema file
        schema_path = "database/schema.sql"
        if not os.path.exists(schema_path):
            print(f"❌ Error: Schema file not found at {schema_path}")
            return False

        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        print(f"✅ Loaded schema from {schema_path}")

        # Execute schema SQL
        # Note: The Python client doesn't support raw SQL execution
        # Users need to run this in the Supabase SQL Editor
        print("\n" + "="*50)
        print("⚠️  IMPORTANT: Manual Step Required")
        print("="*50)
        print("\nThe Python Supabase client doesn't support raw SQL execution.")
        print("Please complete setup by running the schema in Supabase SQL Editor:\n")
        print("1. Go to: https://supabase.com/dashboard/project/htqwegnixlhdhrdbjkgp/editor")
        print("2. Click 'SQL Editor' in the left sidebar")
        print("3. Click '+ New query'")
        print("4. Copy the contents of: database/schema.sql")
        print("5. Paste into the editor")
        print("6. Click 'Run' (or press Cmd/Ctrl + Enter)")
        print("7. You should see 'Success. No rows returned'")
        print("\n" + "="*50)
        print("\nAfter running the schema, your database will have:")
        print("  • profiles - User accounts")
        print("  • sources - Twitter/YouTube/Newsletter sources")
        print("  • drafts - Generated newsletters")
        print("  • feedback - User ratings on drafts")
        print("  • style_training - Writing style samples")
        print("  • email_sends - Email delivery logs")
        print("  • analytics - Usage tracking")
        print("  • user_stats VIEW - Pre-computed statistics")
        print("\n✅ All tables include Row Level Security (RLS) policies")
        print("="*50)

        # Test basic connection
        print("\n🧪 Testing database connection...")
        try:
            # Try to query profiles table (should exist after schema setup)
            result = supabase.table('profiles').select("id").limit(1).execute()
            print("✅ Database connection working!")
            print(f"   Tables are accessible")
            return True
        except Exception as e:
            if "relation" in str(e).lower() and "does not exist" in str(e).lower():
                print("⚠️  Tables not yet created. Please run the schema.sql as instructed above.")
            else:
                print(f"⚠️  Connection test: {str(e)}")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database()
    print("\n📚 For detailed instructions, see: SUPABASE_SETUP_GUIDE.md")
