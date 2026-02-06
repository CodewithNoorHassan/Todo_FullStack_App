# TaskMaster API Documentation

## Overview

The TaskMaster API provides a secure, scalable backend for the premium todo application. The API uses JWT-based authentication and enforces strict user data isolation.

## Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

Tokens are obtained through the Better Auth frontend integration.

## Base URL

```
http://localhost:8000/api
```

## Endpoints

### Tasks

#### GET `/tasks`

Retrieve a list of tasks for the authenticated user.

**Parameters:**
- `skip` (int, optional): Number of tasks to skip for pagination (default: 0)
- `limit` (int, optional): Maximum number of tasks to return (default: 20, max: 100)
- `completed` (bool, optional): Filter by completion status

**Response:**
```json
[
  {
    "id": 1,
    "title": "Sample task",
    "description": "Task description",
    "completed": false,
    "user_id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

#### POST `/tasks`

Create a new task for the authenticated user.

**Request Body:**
```json
{
  "title": "New task",
  "description": "Task description",
  "completed": false
}
```

**Response:**
```json
{
  "id": 1,
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "user_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### GET `/tasks/{task_id}`

Retrieve a specific task by ID.

**Path Parameters:**
- `task_id` (int): ID of the task to retrieve

**Response:**
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Task description",
  "completed": false,
  "user_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### PUT `/tasks/{task_id}`

Update a specific task by ID.

**Path Parameters:**
- `task_id` (int): ID of the task to update

**Request Body:**
```json
{
  "title": "Updated task",
  "description": "Updated description",
  "completed": true
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated task",
  "description": "Updated description",
  "completed": true,
  "user_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### DELETE `/tasks/{task_id}`

Delete a specific task by ID.

**Path Parameters:**
- `task_id` (int): ID of the task to delete

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

#### PATCH `/tasks/{task_id}/toggle`

Toggle the completion status of a specific task.

**Path Parameters:**
- `task_id` (int): ID of the task to toggle

**Response:**
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Task description",
  "completed": true,
  "user_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### Authentication

#### GET `/auth/me`

Get information about the currently authenticated user.

**Response:**
```json
{
  "message": "User info endpoint - integration with Better Auth needed"
}
```

#### GET `/auth/status`

Get authentication status of the current session.

**Response:**
```json
{
  "authenticated": true,
  "provider": "Better Auth"
}
```

### Health

#### GET `/health`

Check the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0"
}
```

## Error Responses

The API returns consistent error responses in the following format:

```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized (invalid/missing JWT)
- `403`: Forbidden (cross-user access attempt)
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

## Security

- All endpoints require valid JWT authentication
- Users can only access their own data
- Requests without proper authentication return 401
- Cross-user access attempts return 403
- Input is validated using Pydantic models