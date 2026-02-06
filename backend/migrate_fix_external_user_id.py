#!/usr/bin/env python3
"""
Migration script to fix external_user_id column to allow NULL values.
"""
import os
from sqlalchemy import text, create_engine
import sys

def fix_external_user_id():
    """Fix external_user_id column to be nullable."""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not set!")
        print("Please set DATABASE_URL before running this migration.")
        return False

    print("🔧 Fixing external_user_id column to be nullable...")
    print(f"📊 Using database URL from environment variable")

    try:
        engine = create_engine(database_url)

        with engine.begin() as connection:
            # Remove the NOT NULL constraint from external_user_id
            print("🔗 Connecting to database...")

            # Check if column exists
            print("🔍 Checking if column exists...")
            result = connection.execute(
                text("SELECT column_name FROM information_schema.columns WHERE table_name='user' AND column_name='external_user_id'")
            )

            if result.fetchone():
                print("✏️ Modifying external_user_id column to allow NULL...")
                connection.execute(
                    text("ALTER TABLE \"user\" ALTER COLUMN external_user_id DROP NOT NULL")
                )
                print("✅ Column modified successfully!")
            else:
                print("⚠️ Column does not exist, skipping...")

        print("✅ Migration completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

if __name__ == "__main__":
    success = fix_external_user_id()
    sys.exit(0 if success else 1)
