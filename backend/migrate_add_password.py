#!/usr/bin/env python3
"""
Add hashed_password column to existing user table.
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def migrate_add_password():
    """Add hashed_password column to user table if it doesn't exist."""
    from sqlmodel import create_engine, Session, text
    from app.config import settings
    
    print("🔧 Adding hashed_password column to user table...")
    print(f"📊 Database URL: {settings.database_url[:50]}...")
    
    # Create engine with shorter timeout
    engine = create_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        connect_args={
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 3,
        } if "postgresql" in settings.database_url else {}
    )
    
    try:
        with Session(engine) as session:
            print("🔗 Connecting to database...")
            
            # Check if column already exists
            print("🔍 Checking if column exists...")
            result = session.exec(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user' 
                AND column_name = 'hashed_password'
            """)).first()
            
            if result:
                print("✅ Column 'hashed_password' already exists!")
                return True
            
            # Column doesn't exist, add it
            print("➕ Adding 'hashed_password' column...")
            session.exec(text("""
                ALTER TABLE "user" 
                ADD COLUMN hashed_password VARCHAR(500)
            """))
            session.commit()
            print("✅ Column added successfully!")
            
            # Verify
            print("🔍 Verifying column...")
            result = session.exec(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user' 
                AND column_name = 'hashed_password'
            """)).first()
            
            if result:
                print("✅ Migration completed successfully!")
                return True
            else:
                print("❌ Column verification failed!")
                return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate_add_password()
    sys.exit(0 if success else 1)
