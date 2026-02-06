#!/usr/bin/env python3
"""
End-to-End Integration Test
Tests the full workflow: signup → create todo → create task → view dashboard
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8001"
API_URL = f"{BASE_URL}/api"

# Test user credentials
TEST_EMAIL = f"test-{int(time.time())}@example.com"
TEST_PASSWORD = "TestPassword123"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    """Test health endpoint"""
    print_section("1. Testing Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✓ Health check: {response.status_code}")
        print(f"  Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_signup(email, password):
    """Test user signup"""
    print_section("2. Testing User Signup")
    try:
        payload = {
            "email": email,
            "password": password,
            "name": "Test User"
        }
        response = requests.post(f"{API_URL}/auth/register", json=payload)
        print(f"✓ Signup: {response.status_code}")
        data = response.json()
        token = data.get("token")
        user_id = data.get("user", {}).get("id")
        print(f"  Token: {token[:20]}...")
        print(f"  User ID: {user_id}")
        return token, user_id
    except Exception as e:
        print(f"✗ Signup failed: {e}")
        return None, None

def test_create_todo(token):
    """Test creating a todo/project"""
    print_section("3. Testing Create Todo/Project")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "title": "My First Project",
            "description": "Testing the full integration"
        }
        response = requests.post(f"{API_URL}/todos", json=payload, headers=headers)
        print(f"✓ Create todo: {response.status_code}")
        data = response.json()
        todo_id = data.get("id")
        print(f"  Todo ID: {todo_id}")
        print(f"  Title: {data.get('title')}")
        return todo_id
    except Exception as e:
        print(f"✗ Create todo failed: {e}")
        return None

def test_create_task(token, todo_id):
    """Test creating a task"""
    print_section("4. Testing Create Task")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        payload = {
            "title": "Complete integration test",
            "description": "Verify all API endpoints work correctly",
            "todo_id": todo_id,
            "status": "TODO",
            "priority": "HIGH",
            "due_date": due_date
        }
        response = requests.post(f"{API_URL}/tasks", json=payload, headers=headers)
        print(f"✓ Create task: {response.status_code}")
        data = response.json()
        task_id = data.get("id")
        print(f"  Task ID: {task_id}")
        print(f"  Title: {data.get('title')}")
        print(f"  Status: {data.get('status')}")
        print(f"  Priority: {data.get('priority')}")
        return task_id
    except Exception as e:
        print(f"✗ Create task failed: {e}")
        return None

def test_get_tasks(token):
    """Test getting tasks list"""
    print_section("5. Testing Get Tasks List")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/tasks?skip=0&limit=50", headers=headers)
        print(f"✓ Get tasks: {response.status_code}")
        data = response.json()
        tasks = data.get("tasks", [])
        print(f"  Total tasks: {data.get('total')}")
        print(f"  Retrieved: {len(tasks)}")
        if tasks:
            task = tasks[0]
            print(f"  First task: {task.get('title')} ({task.get('status')})")
        return len(tasks) > 0
    except Exception as e:
        print(f"✗ Get tasks failed: {e}")
        return False

def test_update_task_status(token, task_id):
    """Test updating task status"""
    print_section("6. Testing Update Task Status")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"status": "IN_PROGRESS"}
        response = requests.put(f"{API_URL}/tasks/{task_id}", json=payload, headers=headers)
        print(f"✓ Update task: {response.status_code}")
        data = response.json()
        print(f"  New status: {data.get('status')}")
        return data.get('status') == 'IN_PROGRESS'
    except Exception as e:
        print(f"✗ Update task failed: {e}")
        return False

def test_get_dashboard(token):
    """Test dashboard endpoint"""
    print_section("7. Testing Dashboard Endpoint")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/dashboard", headers=headers)
        print(f"✓ Get dashboard: {response.status_code}")
        data = response.json()
        stats = data.get("stats", {})
        print(f"  Total tasks: {stats.get('total_tasks')}")
        print(f"  Completed: {stats.get('completed_tasks')}")
        print(f"  Completion %: {stats.get('completion_percentage'):.1f}%")
        print(f"  Recent tasks: {len(data.get('recent_tasks', []))}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Get dashboard failed: {e}")
        return False

def test_get_todos(token):
    """Test getting todos list"""
    print_section("8. Testing Get Todos List")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/todos?skip=0&limit=50", headers=headers)
        print(f"✓ Get todos: {response.status_code}")
        data = response.json()
        todos = data.get("todos", [])
        print(f"  Total todos: {data.get('total')}")
        print(f"  Retrieved: {len(todos)}")
        if todos:
            todo = todos[0]
            print(f"  First todo: {todo.get('title')}")
        return len(todos) > 0
    except Exception as e:
        print(f"✗ Get todos failed: {e}")
        return False

def main():
    print_section("Full Stack Integration Test")
    print(f"Test Email: {TEST_EMAIL}")
    print(f"Backend: {BASE_URL}")
    
    results = {}
    
    # 1. Health check
    results["health"] = test_health()
    
    # 2. Signup
    token, user_id = test_signup(TEST_EMAIL, TEST_PASSWORD)
    if not token:
        print("\n✗ Cannot continue - signup failed")
        return
    
    # 3. Create todo
    todo_id = test_create_todo(token)
    if not todo_id:
        print("\n✗ Cannot continue - todo creation failed")
        return
    
    # 4. Create task
    task_id = test_create_task(token, todo_id)
    results["create_task"] = task_id is not None
    
    # 5. Get tasks
    results["get_tasks"] = test_get_tasks(token)
    
    # 6. Update task
    if task_id:
        results["update_task"] = test_update_task_status(token, task_id)
    
    # 7. Dashboard
    results["dashboard"] = test_get_dashboard(token)
    
    # 8. Get todos
    results["get_todos"] = test_get_todos(token)
    
    # Print summary
    print_section("Test Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Passed: {passed}/{total}\n")
    for test_name, result in results.items():
        status = "✓" if result else "✗"
        print(f"  {status} {test_name}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(main())
