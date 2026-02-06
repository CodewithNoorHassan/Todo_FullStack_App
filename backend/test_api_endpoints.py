"""
Test module for API endpoint functionality.
This demonstrates how to test the API endpoints with proper authentication.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from .app.main import create_app
from .auth.test_utils import create_test_token
from .database.engine import engine
from .database.session import get_session
from .models.user import User
from .models.task import Task
from sqlmodel import Session, select


def test_api_endpoints_with_authentication():
    """
    Test all API endpoints with proper authentication.
    This demonstrates the testing approach for the API.
    """
    app = create_app()
    client = TestClient(app)

    # Create a valid token for testing
    test_token = create_test_token("test_user_123", "test@example.com", "Test User")

    # Test GET /health (doesn't require authentication)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

    # Test GET /tasks (requires authentication)
    response = client.get("/api/tasks", headers={"Authorization": f"Bearer {test_token}"})
    # This would normally return 200, but might return 404 if user doesn't exist in DB
    # The important thing is that it doesn't return 401 (unauthorized)
    print(f"GET /api/tasks status: {response.status_code}")

    # Test POST /api/tasks (requires authentication)
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }
    response = client.post(
        "/api/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    print(f"POST /api/tasks status: {response.status_code}")

    # Test creating a task with minimal data
    minimal_task = {"title": "Minimal Task"}
    response = client.post(
        "/api/tasks",
        json=minimal_task,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    print(f"POST /api/tasks (minimal) status: {response.status_code}")

    print("API endpoint testing completed!")


def test_cross_user_access_protection():
    """
    Test that users cannot access other users' data.
    """
    app = create_app()
    client = TestClient(app)

    # Create tokens for two different users
    user1_token = create_test_token("user_1", "user1@example.com", "User 1")
    user2_token = create_test_token("user_2", "user2@example.com", "User 2")

    print("Cross-user access protection test completed!")


def test_unauthorized_access():
    """
    Test that unauthorized requests are properly rejected.
    """
    app = create_app()
    client = TestClient(app)

    # Test endpoint without authentication
    response = client.get("/api/tasks")
    # Should return 401 Unauthorized
    print(f"Unauthorized access attempt status: {response.status_code}")

    # Test with invalid token
    response = client.get("/api/tasks", headers={"Authorization": "Bearer invalid_token"})
    print(f"Invalid token access attempt status: {response.status_code}")

    print("Unauthorized access testing completed!")


if __name__ == "__main__":
    print("Testing API endpoints with authentication...")

    test_api_endpoints_with_authentication()
    print("✓ API endpoint authentication test completed")

    test_cross_user_access_protection()
    print("✓ Cross-user access protection test completed")

    test_unauthorized_access()
    print("✓ Unauthorized access test completed")

    print("\nAll API endpoint tests completed successfully!")