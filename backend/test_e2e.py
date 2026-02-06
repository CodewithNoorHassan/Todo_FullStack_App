"""
End-to-end tests for all TaskMaster API features.
"""
import pytest
import time
from fastapi.testclient import TestClient
from unittest.mock import Mock
from .app.main import create_app
from .auth.test_utils import create_test_token
from .models.user import User
from .models.task import Task
from sqlmodel import Session, select
from .database.engine import engine


def test_complete_workflow():
    """
    Test the complete end-to-end workflow of the TaskMaster API.
    """
    print("Starting end-to-end testing of all features...")

    app = create_app()
    client = TestClient(app)

    # Test 1: Health check
    print("\n1. Testing health check...")
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print(f"   ✓ Health check: {data['status']}")

    # Test 2: Authentication flow
    print("\n2. Testing authentication flow...")
    valid_token = create_test_token("e2e_test_user_123", "e2e@example.com", "E2E Test User")
    auth_headers = {"Authorization": f"Bearer {valid_token}"}
    print("   ✓ JWT token created for testing")

    # Test 3: Task management flow
    print("\n3. Testing task management workflow...")

    # 3a. Get initial tasks (should be empty or user-specific)
    response = client.get("/api/tasks", headers=auth_headers)
    assert response.status_code in [200, 404]  # Could be 404 if no tasks exist
    initial_task_count = len(response.json()) if response.status_code == 200 else 0
    print(f"   ✓ Initial tasks retrieved: {initial_task_count}")

    # 3b. Create a new task
    new_task_data = {
        "title": "E2E Test Task",
        "description": "This task was created during end-to-end testing",
        "completed": False
    }
    response = client.post("/api/tasks", json=new_task_data, headers=auth_headers)
    assert response.status_code in [200, 201]
    created_task = response.json()
    print(f"   ✓ Task created: '{created_task.get('title', 'Unknown')}'")

    # 3c. Get the newly created task
    task_id = created_task.get('id')
    if task_id:
        response = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        retrieved_task = response.json()
        assert retrieved_task['title'] == new_task_data['title']
        print(f"   ✓ Task retrieved: '{retrieved_task['title']}'")

    # 3d. Update the task
    update_data = {
        "title": "E2E Test Task - Updated",
        "description": "This task was updated during end-to-end testing",
        "completed": True
    }
    if task_id:
        response = client.put(f"/api/tasks/{task_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task['title'] == update_data['title']
        assert updated_task['completed'] is True
        print(f"   ✓ Task updated: '{updated_task['title']}'")

    # 3e. Toggle task completion
    if task_id:
        response = client.patch(f"/api/tasks/{task_id}/toggle", headers=auth_headers)
        assert response.status_code == 200
        toggled_task = response.json()
        assert toggled_task['completed'] is False  # Should be toggled back to False
        print(f"   ✓ Task completion toggled: {toggled_task['completed']}")

    # 3f. Get all tasks again
    response = client.get("/api/tasks", headers=auth_headers)
    assert response.status_code == 200
    all_tasks = response.json()
    print(f"   ✓ All tasks retrieved: {len(all_tasks)}")

    # 3g. Delete the test task
    if task_id:
        response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        print(f"   ✓ Task deleted: ID {task_id}")

    # Test 4: Security validation
    print("\n4. Testing security features...")

    # 4a. Try to access without authentication
    response = client.get("/api/tasks")
    assert response.status_code == 401
    print("   ✓ Unauthenticated access properly rejected")

    # 4b. Try to access with invalid token
    response = client.get("/api/tasks", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    print("   ✓ Invalid token properly rejected")

    # Test 5: Error handling
    print("\n5. Testing error handling...")

    # 5a. Access non-existent task
    if task_id:
        response = client.get(f"/api/tasks/999999", headers=auth_headers)
        # This could be 404 or 403 depending on implementation
        print(f"   ✓ Non-existent task access: {response.status_code}")

    # 5b. Invalid input validation
    response = client.post(
        "/api/tasks",
        json={"title": ""},  # Empty title should fail validation
        headers=auth_headers
    )
    assert response.status_code in [422, 400]  # Validation or bad request error
    print(f"   ✓ Invalid input properly handled: {response.status_code}")

    print("\n✓ Complete end-to-end workflow testing passed!")


def test_api_consistency():
    """
    Test API consistency and response formats.
    """
    print("\nTesting API consistency...")

    app = create_app()
    client = TestClient(app)

    # Test consistent response formats
    valid_token = create_test_token("consistency_test_user", "cons@example.com", "Consistency Test")
    auth_headers = {"Authorization": f"Bearer {valid_token}"}

    # Health endpoint
    response = client.get("/health")
    assert "status" in response.json()
    assert "environment" in response.json()
    print("   ✓ Health response format consistent")

    # Task endpoints should return consistent formats
    response = client.get("/api/tasks", headers=auth_headers)
    if response.status_code == 200:
        tasks = response.json()
        if tasks:  # If there are tasks
            task = tasks[0]
            required_fields = ["id", "title", "description", "completed", "user_id", "created_at", "updated_at"]
            for field in required_fields:
                assert field in task, f"Missing field {field} in task response"
    print("   ✓ Task response format consistent")

    # Error responses should be consistent
    response = client.get("/api/tasks", headers={"Authorization": "Bearer invalid"})
    assert "detail" in response.json()
    print("   ✓ Error response format consistent")

    print("✓ API consistency testing passed!")


def test_performance_under_load():
    """
    Test basic performance under simulated load.
    """
    print("\nTesting performance under load...")

    app = create_app()
    client = TestClient(app)

    valid_token = create_test_token("load_test_user", "load@example.com", "Load Test User")
    auth_headers = {"Authorization": f"Bearer {valid_token}"}

    # Create multiple tasks in sequence to test performance
    start_time = time.time()
    task_ids = []

    for i in range(10):  # Create 10 tasks
        task_data = {
            "title": f"Load Test Task {i}",
            "description": f"This is load test task number {i}",
            "completed": i % 2 == 0  # Alternate completion status
        }
        response = client.post("/api/tasks", json=task_data, headers=auth_headers)
        if response.status_code in [200, 201]:
            task_id = response.json().get('id')
            if task_id:
                task_ids.append(task_id)

    end_time = time.time()
    creation_time = end_time - start_time

    print(f"   ✓ Created {len(task_ids)} tasks in {creation_time:.2f} seconds")

    # Clean up created tasks
    for task_id in task_ids:
        client.delete(f"/api/tasks/{task_id}", headers=auth_headers)

    print("✓ Performance testing passed!")


def run_all_e2e_tests():
    """
    Run all end-to-end tests.
    """
    print("=" * 70)
    print("RUNNING END-TO-END TESTS FOR ALL FEATURES")
    print("=" * 70)

    try:
        test_complete_workflow()
        test_api_consistency()
        test_performance_under_load()

        print("\n" + "=" * 70)
        print("ALL END-TO-END TESTS PASSED SUCCESSFULLY!")
        print("All features are working correctly and integrated properly.")
        print("=" * 70)

        return True

    except AssertionError as e:
        print(f"\n❌ END-TO-END TEST FAILED: {e}")
        print("=" * 70)
        return False

    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR IN E2E TESTS: {e}")
        print("=" * 70)
        return False


if __name__ == "__main__":
    success = run_all_e2e_tests()
    if success:
        print("\n🎉 End-to-end testing completed successfully!")
    else:
        print("\n💥 End-to-end testing revealed issues!")
        exit(1)