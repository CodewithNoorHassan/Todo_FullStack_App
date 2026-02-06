#!/usr/bin/env python3
"""
Database initialization script for Neon PostgreSQL.
Creates all tables and initializes the database schema.
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def init_db():
    """Initialize the database with all required tables."""
    from sqlmodel import SQLModel, create_engine, Session
    from app.config import settings
    from models.user import User
    from models.todo import Todo
    from models.task import Task
    
    print("🚀 Starting database initialization...")
    print(f"📊 Database URL: {settings.database_url[:50]}...")
    
    # Create engine
    engine = create_engine(
        settings.database_url,
        echo=True,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=30,
        pool_recycle=3600,
        connect_args={
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 3,
        } if "postgresql" in settings.database_url else {}
    )
    
    try:
        # Create all tables
        print("📝 Creating tables...")
        SQLModel.metadata.create_all(engine)
        print("✅ Database tables created successfully!")
        
        # Test connection
        with Session(engine) as session:
            from sqlalchemy import text
            print("🔗 Testing database connection...")
            session.exec(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        print("\n✨ Database initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)
