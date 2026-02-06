# Frontend Integration Guide

## Overview

This guide provides everything needed for the frontend team to integrate with the TaskMaster API backend. It covers authentication, API endpoints, error handling, and best practices for seamless integration.

## Base URLs

### Development
```
BASE_URL = http://localhost:8000
```

### Production
```
BASE_URL = https://api.yourdomain.com
```

## Authentication Integration

### With Better Auth

The backend is designed to work with Better Auth for user management:

1. **User Registration/Login**: Handle through Better Auth frontend
2. **JWT Token**: Better Auth provides JWT tokens after successful authentication
3. **API Requests**: Include JWT in Authorization header for all API requests

### Authorization Header Format

```
Authorization: Bearer <jwt_token_here>
```

### Example Implementation (JavaScript)
```javascript
// Get the JWT token from Better Auth after successful login
const authToken = await betterAuth.getToken(); // Or however you get the token

// Make API requests with the token
const response = await fetch('http://localhost:8000/api/tasks', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${authToken}`,
    'Content-Type': 'application/json'
  }
});
```

## API Endpoints

### Health Check Endpoints (No Auth Required)

#### GET `/health`
**Purpose**: Check API health status
```javascript
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));
// Response: { "status": "healthy", "environment": "development", "version": "1.0.0" }
```

#### GET `/ready`
**Purpose**: Check if API is ready to serve requests
```javascript
fetch('http://localhost:8000/ready')
  .then(response => response.json())
  .then(data => console.log(data));
// Response: { "status": "ready" }
```

### Task Management Endpoints (Auth Required)

#### GET `/api/tasks`
**Purpose**: Get list of tasks for the authenticated user
**Query Parameters**:
- `skip` (optional): Number of tasks to skip for pagination (default: 0)
- `limit` (optional): Maximum number of tasks to return (default: 20, max: 100)
- `completed` (optional): Filter by completion status (true/false)

```javascript
// Get all tasks
fetch('http://localhost:8000/api/tasks', {
  headers: {
    'Authorization': `Bearer ${authToken}`
  }
})
.then(response => response.json())
.then(tasks => console.log(tasks));

// Get completed tasks only
fetch('http://localhost:8000/api/tasks?completed=true&limit=10', {
  headers: {
    'Authorization': `Bearer ${authToken}`
  }
})
.then(response => response.json())
.then(tasks => console.log(tasks));
```

#### POST `/api/tasks`
**Purpose**: Create a new task
**Request Body**:
```javascript
{
  "title": "Task title (required)",
  "description": "Task description (optional)",
  "completed": false (optional, default: false)
}
```

```javascript
const newTask = {
  title: "New Task",
  description: "Task description",
  completed: false
};

fetch('http://localhost:8000/api/tasks', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${authToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(newTask)
})
.then(response => response.json())
.then(createdTask => console.log(createdTask));
```

#### GET `/api/tasks/{task_id}`
**Purpose**: Get a specific task
```javascript
fetch('http://localhost:8000/api/tasks/123', {
  headers: {
    'Authorization': `Bearer ${authToken}`
  }
})
.then(response => response.json())
.then(task => console.log(task));
```

#### PUT `/api/tasks/{task_id}`
**Purpose**: Update a specific task
**Request Body** (all fields optional, only provided fields are updated):
```javascript
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

```javascript
const updatedTask = {
  title: "Updated Task Title",
  completed: true
};

fetch('http://localhost:8000/api/tasks/123', {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${authToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(updatedTask)
})
.then(response => response.json())
.then(task => console.log(task));
```

#### PATCH `/api/tasks/{task_id}/toggle`
**Purpose**: Toggle the completion status of a task
```javascript
fetch('http://localhost:8000/api/tasks/123/toggle', {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${authToken}`
  }
})
.then(response => response.json())
.then(toggledTask => console.log(toggledTask));
```

#### DELETE `/api/tasks/{task_id}`
**Purpose**: Delete a specific task
```javascript
fetch('http://localhost:8000/api/tasks/123', {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${authToken}`
  }
})
.then(response => {
  if (response.ok) {
    console.log('Task deleted successfully');
  }
});
```

### Authentication Status Endpoints (Auth Required)

#### GET `/api/auth/me`
**Purpose**: Get current user information
```javascript
fetch('http://localhost:8000/api/auth/me', {
  headers: {
    'Authorization': `Bearer ${authToken}`
  }
})
.then(response => response.json())
.then(userInfo => console.log(userInfo));
```

#### GET `/api/auth/status`
**Purpose**: Get authentication status
```javascript
fetch('http://localhost:8000/api/auth/status', {
  headers: {
    'Authorization': `Bearer ${authToken}`
  }
})
.then(response => response.json())
.then(authStatus => console.log(authStatus));
```

## Error Handling

### Common Error Responses

All error responses follow the format:
```javascript
{
  "detail": "Error message explaining what went wrong"
}
```

### HTTP Status Codes

| Status Code | Meaning | Action |
|-------------|---------|---------|
| 200 | Success | Normal operation |
| 201 | Created | Resource successfully created |
| 400 | Bad Request | Check request parameters/format |
| 401 | Unauthorized | Token is invalid or missing, redirect to login |
| 403 | Forbidden | User tried to access resources they don't own |
| 404 | Not Found | Requested resource doesn't exist |
| 422 | Validation Error | Request body failed validation |
| 500 | Internal Server Error | Something went wrong on the server |

### Error Handling Best Practices

```javascript
async function makeApiCall(url, options = {}) {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });

    if (!response.ok) {
      const errorData = await response.json();

      switch (response.status) {
        case 401:
          // Token expired or invalid, redirect to login
          redirectToLogin();
          break;
        case 403:
          // Show user-friendly error message
          showErrorMessage('You do not have permission to access this resource.');
          break;
        case 400:
        case 422:
          // Validation error, show specific error
          showErrorMessage(errorData.detail);
          break;
        case 500:
          // Server error, log and show generic message
          console.error('Server error:', errorData);
          showErrorMessage('Something went wrong. Please try again later.');
          break;
        default:
          showErrorMessage('An unexpected error occurred.');
      }

      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Network error:', error);
    showErrorMessage('Network error. Please check your connection.');
    return null;
  }
}
```

## Response Data Structures

### Task Object
```javascript
{
  "id": 123,
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "user_id": 456,  // Internal user ID
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### Error Object
```javascript
{
  "detail": "Error message"
}
```

### Health Check Response
```javascript
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0"
}
```

## Integration Best Practices

### 1. Token Management
- Store JWT tokens securely (preferably in HttpOnly cookies if possible, otherwise in secure storage)
- Implement token refresh logic
- Handle token expiration gracefully

### 2. Loading States
```javascript
function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await makeApiCall('/api/tasks');
        if (data) {
          setTasks(data);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  // Render loading, error, or tasks
}
```

### 3. Optimistic Updates
For better UX, consider implementing optimistic updates for operations like toggling task completion:

```javascript
const toggleTaskCompletion = async (taskId) => {
  // Optimistically update UI
  setTasks(prevTasks =>
    prevTasks.map(task =>
      task.id === taskId ? { ...task, completed: !task.completed } : task
    )
  );

  try {
    const updatedTask = await makeApiCall(`/api/tasks/${taskId}/toggle`, { method: 'PATCH' });
    if (!updatedTask) {
      // If API call failed, revert the optimistic update
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, completed: !task.completed } : task
        )
      );
    }
  } catch (error) {
    // Revert optimistic update on error
    setTasks(prevTasks =>
      prevTasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      )
    );
  }
};
```

### 4. Error Boundaries
Implement error boundaries to catch and handle errors gracefully:

```javascript
// ErrorBoundary.jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('API Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong with the API.</h1>;
    }

    return this.props.children;
  }
}
```

## Performance Tips

1. **Pagination**: Use the `skip` and `limit` parameters to load tasks in chunks
2. **Filtering**: Use the `completed` parameter to filter tasks on the server side
3. **Caching**: Implement appropriate caching strategies for repeated requests
4. **Debouncing**: Debounce search/filter inputs to reduce API calls

## Troubleshooting

### Common Issues

1. **401 Unauthorized Errors**
   - Verify JWT token is being sent correctly in Authorization header
   - Check if token has expired
   - Ensure token format is `Bearer <token>`

2. **403 Forbidden Errors**
   - Users can only access their own tasks
   - Verify the task belongs to the authenticated user

3. **422 Validation Errors**
   - Check that required fields are provided
   - Verify data types and formats

4. **CORS Issues**
   - Backend is configured to allow all origins for development
   - Update CORS settings for production with specific frontend URL

## Support

For integration questions or issues:
- Check the API documentation at `/docs` or `/redoc`
- Review the validation report at `VALIDATION_REPORT.md`
- Contact the backend team for assistance