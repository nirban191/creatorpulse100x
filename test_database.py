#!/usr/bin/env python3
"""
Quick test script to verify Supabase database connection
"""

import os
from dotenv import load_dotenv
from utils.supabase_client import get_db

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test the database connection and basic operations"""

    print("🔍 Testing Supabase Database Connection...\n")

    # Get database client
    db = get_db()

    # Check if configured
    if not db.is_configured():
        print("❌ Database NOT configured!")
        print("\nPlease add the following to your .env file:")
        print("SUPABASE_URL=https://your-project.supabase.co")
        print("SUPABASE_KEY=your_supabase_anon_key_here")
        return False

    print("✅ Database credentials found!")
    print(f"   URL: {db.url[:30]}...")
    print(f"   Key: {db.key[:20]}...")

    # Test user profile operations
    print("\n📝 Testing User Profile Operations...")
    import uuid
    test_user_id = str(uuid.uuid4())  # Generate proper UUID
    test_email = "test@creatorpulse.com"

    try:
        profile = db.get_or_create_profile(test_user_id, test_email)
        if profile:
            print(f"✅ Profile created/retrieved: {test_email}")
        else:
            print("❌ Failed to create/retrieve profile")
            return False
    except Exception as e:
        print(f"❌ Error with profile: {str(e)}")
        return False

    # Test adding a source
    print("\n📝 Testing Source Operations...")
    try:
        result = db.add_source(test_user_id, 'twitter', 'elonmusk')
        if result.get('success'):
            print("✅ Successfully added Twitter source")
        else:
            print(f"❌ Failed to add source: {result.get('error')}")
    except Exception as e:
        print(f"❌ Error adding source: {str(e)}")

    # Get sources
    try:
        sources = db.get_sources(test_user_id, 'twitter')
        print(f"✅ Retrieved {len(sources)} Twitter sources")
    except Exception as e:
        print(f"❌ Error retrieving sources: {str(e)}")

    # Test saving a draft
    print("\n📝 Testing Draft Operations...")
    try:
        result = db.save_draft(
            test_user_id,
            "Test Newsletter",
            "# Test Content\n\nThis is a test newsletter.",
            "groq",
            1500
        )
        if result.get('success'):
            print("✅ Successfully saved draft")
        else:
            print(f"❌ Failed to save draft: {result.get('error')}")
    except Exception as e:
        print(f"❌ Error saving draft: {str(e)}")

    # Get drafts
    try:
        drafts = db.get_drafts(test_user_id, limit=5)
        print(f"✅ Retrieved {len(drafts)} drafts")
    except Exception as e:
        print(f"❌ Error retrieving drafts: {str(e)}")

    # Test user stats
    print("\n📝 Testing Analytics...")
    try:
        stats = db.get_user_stats(test_user_id)
        print("✅ User Stats:")
        print(f"   - Total Sources: {stats.get('total_sources', 0)}")
        print(f"   - Total Drafts: {stats.get('total_drafts', 0)}")
        print(f"   - Acceptance Rate: {stats.get('acceptance_rate', 0):.1f}%")
        print(f"   - Hours Saved: {stats.get('estimated_hours_saved', 0):.1f}h")
    except Exception as e:
        print(f"❌ Error retrieving stats: {str(e)}")

    print("\n" + "="*50)
    print("✅ All database tests completed successfully!")
    print("="*50)

    return True

if __name__ == "__main__":
    test_database_connection()
