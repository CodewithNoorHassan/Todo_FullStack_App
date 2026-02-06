"""
Test script to debug 500 error on task creation
"""
import requests
import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_task_creation():
    BASE_URL = "http://localhost:8000/api"
    
    # Test credentials
    test_email = "debug@test.com"
    test_password = "debugpass123"
    
    print("=" * 60)
    print("STEP 1: Attempting to register user")
    print("=" * 60)
    
    signup_response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": test_email,
            "password": test_password,
            "name": "Debug User"
        }
    )
    
    print(f"Status: {signup_response.status_code}")
    print(f"Response: {signup_response.text}")
    
    if signup_response.status_code not in [200, 201]:
        print("Registration failed, trying login instead...")
        
    print("\n" + "=" * 60)
    print("STEP 2: Logging in")
    print("=" * 60)
    
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": test_email,
            "password": test_password
        }
    )
    
    print(f"Status: {login_response.status_code}")
    print(f"Response: {login_response.text}")
    
    if login_response.status_code != 200:
        print("❌ Login failed")
        return
    
    auth_data = login_response.json()
    token = auth_data.get("token")
    
    print(f"\nToken obtained: {token[:50]}...")
    
    print("\n" + "=" * 60)
    print("STEP 3: Creating a task")
    print("=" * 60)
    
    task_payload = {
        "title": "Debug Test Task",
        "description": "This is a debug test",
        "priority": "MEDIUM",
        "status": "TODO"
    }
    
    print(f"Payload: {json.dumps(task_payload, indent=2)}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    task_response = requests.post(
        f"{BASE_URL}/tasks",
        json=task_payload,
        headers=headers
    )
    
    print(f"\nStatus: {task_response.status_code}")
    print(f"Headers: {dict(task_response.headers)}")
    print(f"Response: {task_response.text}")
    
    if task_response.status_code != 200:
        print(f"\nX Task creation failed with status {task_response.status_code}")
        
        try:
            error_data = task_response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print("Could not parse error response as JSON")
    else:
        print("\nOK Task created successfully!")
        task_data = task_response.json()
        print(f"Task: {json.dumps(task_data, indent=2)}")

if __name__ == "__main__":
    test_task_creation()
