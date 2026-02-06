#!/usr/bin/env python3
"""
Full integration test to debug task creation
"""
import os
import sys
import json
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def test_full_flow():
    """Test the full task creation flow"""
    from fastapi.testclient import TestClient
    from app.main import create_app
    from sqlmodel import Session
    from database.engine import engine
    from models.user import User
    from models.todo import Todo
    from auth.jwt_handler import create_access_token
    
    print("🧪 Full Integration Test for Task Creation\n")
    
    # Create app
    app = create_app()
    client = TestClient(app)
    
    try:
        # 1. Get a user and create token
        with Session(engine) as session:
            user = session.query(User).first()
            if not user:
                print("❌ No users found in database")
                return False
            
            print(f"✅ Found user: {user.email} (ID: {user.id})")
            
            # Create a valid JWT token
            token_data = {
                "sub": user.email,
                "email": user.email
            }
            try:
                # Try to create token - might fail if secret key doesn't match
                from auth.config import auth_settings
                token = create_access_token(token_data)
                print(f"✅ Created JWT token: {token[:50]}...")
            except Exception as e:
                print(f"⚠️  Could not create token via create_access_token: {e}")
                print("   Using a simpler approach...")
                from jose import jwt
                token = jwt.encode(
                    token_data,
                    auth_settings.BETTER_AUTH_SECRET,
                    algorithm=auth_settings.algorithm
                )
                print(f"✅ Created JWT token: {token[:50]}...")
            
            # Get a todo
            todo = session.query(Todo).filter(Todo.user_id == user.id).first()
            if not todo:
                print("❌ No todos found for user")
                return False
            
            print(f"✅ Found todo: {todo.id} - {todo.title}\n")
        
        # 2. Test the API endpoint
        print("📝 Testing POST /api/tasks endpoint...")
        
        payload = {
            "title": "Integration Test Task",
            "description": "This is a test task from the integration test",
            "todo_id": todo.id,
            "priority": "HIGH",
            "status": "TODO"
        }
        
        print(f"📤 Request payload: {json.dumps(payload, indent=2)}")
        print(f"🔐 Authorization: Bearer {token[:30]}...\n")
        
        response = client.post(
            "/api/tasks",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Body: {response.json()}\n")
        
        if response.status_code == 200:
            print("✅ Task created successfully!")
            return True
        else:
            print(f"❌ Failed to create task")
            print(f"   Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_flow()
    sys.exit(0 if success else 1)
