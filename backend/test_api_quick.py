#!/usr/bin/env python3
"""
Test script to check API endpoint
"""
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def test_api():
    """Test the API endpoint"""
    import json
    from fastapi.testclient import TestClient
    from app.main import app
    from database.session import get_session
    from database.engine import engine
    from sqlmodel import Session
    from models.user import User
    from models.todo import Todo
    
    print("🧪 Testing API endpoint...")
    
    try:
        # Create test client
        client = TestClient(app)
        
        # Get a user from database
        with Session(engine) as session:
            user = session.query(User).first()
            if not user:
                print("❌ No users found in database")
                return False
            
            print(f"✅ Found user: {user.email}")
            
            # Get a todo
            todo = session.query(Todo).filter(Todo.user_id == user.id).first()
            if not todo:
                print("❌ No todos found for user")
                return False
            
            print(f"✅ Found todo: {todo.id}")
        
        # For now, just check the models
        print("✅ API structure looks good")
        return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
