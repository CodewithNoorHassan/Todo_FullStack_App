#!/usr/bin/env python3
"""
Test Neon database connection and configuration.
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def test_connection():
    """Test the Neon database connection."""
    from app.config import settings
    
    print("=" * 60)
    print("🔍 NEON DATABASE CONNECTION TEST")
    print("=" * 60)
    
    print(f"\n📊 App Environment: {settings.APP_ENV}")
    print(f"🔑 JWT Algorithm: {settings.jwt_algorithm}")
    print(f"⏱️  Token Expiry: {settings.access_token_expire_minutes} minutes")
    
    # Hide sensitive parts of connection string
    db_url = settings.database_url
    if "postgresql" in db_url:
        # Hide password
        parts = db_url.split("@")
        if len(parts) == 2:
            visible = f"{parts[0][:30]}...@{parts[1]}"
        else:
            visible = db_url[:50] + "..."
    else:
        visible = db_url
    
    print(f"🗄️  Database URL: {visible}")
    
    try:
        from sqlmodel import create_engine, Session, text
        
        print("\n🔗 Attempting connection to Neon database...")
        
        # Create engine with connection pooling
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
        
        # Test the connection
        with Session(engine) as session:
            result = session.exec(text("SELECT 1")).first()
            
        print("✅ Successfully connected to Neon database!")
        print(f"✅ Connection test returned: {result}")
        print("\n" + "=" * 60)
        print("✨ All configuration tests passed!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
