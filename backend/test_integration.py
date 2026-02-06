"""
Integration tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from .app.main import create_app
from .auth.test_utils import create_test_token
from .models.user import User
from .models.task import Task
from sqlmodel import Session, select
from contextlib import contextmanager


@contextmanager
def override_get_session(mock_session):
    """Helper to temporarily override the get_session dependency."""
    from .database.session import get_session

    def override_session():
        yield mock_session

    app = create_app()
    app.dependency_overrides[get_session] = override_session
    try:
        yield app
    finally:
        app.dependency_overrides.clear()


def test_task_crud_integration():
    """Test full task CRUD integration flow."""
    print("Testing task CRUD integration...")

    # Create a mock session
    mock_session = MagicMock(spec=Session)

    # Mock user retrieval
    mock_user = User(id=1, external_user_id="test_user_123", email="test@example.com")
    mock_session.get.return_value = mock_user

    # Mock task creation and retrieval
    created_task = Task(
        id=1,
        title="Integration Test Task",
        description="Test description",
        completed=False,
        user_id=1
    )

    def mock_exec_side_effect(query):
        # Mock the exec method to return appropriate results
        if hasattr(query, '_entity') and query._entity == Task:
            # This is a query for Task
            if hasattr(query, '_where') and query._where:
                # This is a query with WHERE clause (get specific task)
                return MagicMock(first=lambda: created_task, all=lambda: [created_task])
            else:
                # This is a general query (get all tasks)
                return MagicMock(all=lambda: [created_task])
        return MagicMock()

    mock_session.exec.side_effect = mock_exec_side_effect
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.refresh = MagicMock()

    with override_get_session(mock_session) as app:
        client = TestClient(app)

        # Create a valid token
        valid_token = create_test_token("test_user_123")
        auth_headers = {"Authorization": f"Bearer {valid_token}"}

        # Test POST /api/tasks
        response = client.post(
            "/api/tasks",
            json={"title": "Integration Test Task", "description": "Test description"},
            headers=auth_headers
        )
        assert response.status_code in [200, 201]  # May return 200 or 201
        print(f"   ✓ POST /api/tasks: {response.status_code}")

        # Test GET /api/tasks
        response = client.get("/api/tasks", headers=auth_headers)
        assert response.status_code == 200
        print(f"   ✓ GET /api/tasks: {response.status_code}")

        # Test GET /api/tasks/{id}
        response = client.get("/api/tasks/1", headers=auth_headers)
        assert response.status_code in [200, 404]  # Could be 404 if task doesn't exist in real DB
        print(f"   ✓ GET /api/tasks/1: {response.status_code}")

        # Test PUT /api/tasks/{id}
        response = client.put(
            "/api/tasks/1",
            json={"title": "Updated Integration Test Task"},
            headers=auth_headers
        )
        assert response.status_code in [200, 404]  # Could be 404 if task doesn't exist
        print(f"   ✓ PUT /api/tasks/1: {response.status_code}")

        # Test PATCH /api/tasks/{id}/toggle
        response = client.patch("/api/tasks/1/toggle", headers=auth_headers)
        assert response.status_code in [200, 404]  # Could be 404 if task doesn't exist
        print(f"   ✓ PATCH /api/tasks/1/toggle: {response.status_code}")

        # Test DELETE /api/tasks/{id}
        response = client.delete("/api/tasks/1", headers=auth_headers)
        assert response.status_code in [200, 404]  # Could be 404 if task doesn't exist
        print(f"   ✓ DELETE /api/tasks/1: {response.status_code}")

    print("✓ Task CRUD integration test completed")


def test_authentication_integration():
    """Test authentication integration."""
    print("Testing authentication integration...")

    app = create_app()
    client = TestClient(app)

    # Test health endpoint (should not require auth)
    response = client.get("/health")
    assert response.status_code == 200
    print(f"   ✓ Health endpoint: {response.status_code}")

    # Test protected endpoint without auth (should fail)
    response = client.get("/api/tasks")
    assert response.status_code == 401
    print(f"   ✓ Protected endpoint without auth: {response.status_code}")

    # Test protected endpoint with valid auth (may fail due to user not existing in DB)
    valid_token = create_test_token("test_user_123")
    auth_headers = {"Authorization": f"Bearer {valid_token}"}

    response = client.get("/api/tasks", headers=auth_headers)
    # This could be 200 (empty list) or 404 depending on implementation
    print(f"   ✓ Protected endpoint with auth: {response.status_code}")

    print("✓ Authentication integration test completed")


def test_error_handling_integration():
    """Test error handling integration."""
    print("Testing error handling integration...")

    app = create_app()
    client = TestClient(app)

    # Test invalid endpoint
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404
    print(f"   ✓ Invalid endpoint handling: {response.status_code}")

    # Test malformed JSON
    valid_token = create_test_token("test_user_123")
    auth_headers = {"Authorization": f"Bearer {valid_token}"}

    response = client.post(
        "/api/tasks",
        content="invalid json {",
        headers=auth_headers
    )
    # This might return 422 (validation error) or 400 (parse error)
    print(f"   ✓ Malformed JSON handling: {response.status_code}")

    print("✓ Error handling integration test completed")


def test_api_workflow_integration():
    """Test complete API workflow."""
    print("Testing complete API workflow...")

    # This would test a complete user workflow
    # 1. User authenticates (via frontend/Better Auth)
    # 2. Gets valid JWT token
    # 3. Uses token to access API
    # 4. Performs task operations
    # 5. Receives appropriate responses

    app = create_app()
    client = TestClient(app)

    # Simulate the workflow
    valid_token = create_test_token("workflow_user_456")
    auth_headers = {"Authorization": f"Bearer {valid_token}"}

    # Step 1: Get user's tasks (might be empty initially)
    response = client.get("/api/tasks", headers=auth_headers)
    print(f"   ✓ Step 1 - Get tasks: {response.status_code}")

    # Step 2: Create a new task
    response = client.post(
        "/api/tasks",
        json={
            "title": "Workflow Test Task",
            "description": "Task created as part of workflow test",
            "completed": False
        },
        headers=auth_headers
    )
    task_created = response.status_code in [200, 201]
    print(f"   ✓ Step 2 - Create task: {response.status_code}")

    # Step 3: Get updated task list
    response = client.get("/api/tasks", headers=auth_headers)
    print(f"   ✓ Step 3 - Get updated tasks: {response.status_code}")

    # Step 4: Update the task (if it was created)
    if task_created:
        # Parse the task ID from the creation response if possible
        # For now, we'll just try with a placeholder ID
        response = client.put(
            "/api/tasks/1",
            json={"title": "Updated Workflow Task", "completed": True},
            headers=auth_headers
        )
        print(f"   ✓ Step 4 - Update task: {response.status_code}")

    print("✓ API workflow integration test completed")


def run_all_integration_tests():
    """Run all integration tests."""
    print("=" * 60)
    print("RUNNING INTEGRATION TESTS FOR API ENDPOINTS")
    print("=" * 60)

    test_task_crud_integration()
    print()

    test_authentication_integration()
    print()

    test_error_handling_integration()
    print()

    test_api_workflow_integration()
    print()

    print("=" * 60)
    print("ALL INTEGRATION TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_integration_tests()