# Backend API Specification: Premium Todo Application

**Version**: 1.0.0 | **Date**: 2026-01-30 | **Status**: Active

## Overview

Premium Todo Application backend provides RESTful API for task and todo management with secure JWT-based authentication. The backend serves the Next.js frontend with complete CRUD operations, user authentication, and dashboard analytics.

---

## Architecture

**Framework**: FastAPI (Python)
**Database**: Neon PostgreSQL (Serverless)
**Authentication**: JWT (HS256) with Better Auth
**ORM**: SQLModel (SQLAlchemy + Pydantic)
**API Style**: REST
**Port**: 8001

---

## Core Entities

### User
- **Purpose**: User authentication and profile management
- **Attributes**:
  - `id`: Integer (Primary Key)
  - `external_user_id`: String, Optional, Unique (Better Auth integration)
  - `email`: String, Unique, Required
  - `name`: String, Optional
  - `hashed_password`: String (bcrypt), Required for JWT auth
  - `created_at`: Datetime
  - `updated_at`: Datetime

### Todo
- **Purpose**: High-level todo lists/projects
- **Attributes**:
  - `id`: Integer (Primary Key)
  - `user_id`: Integer (Foreign Key to User)
  - `title`: String, Required
  - `description`: String, Optional
  - `color`: String (hex code), Optional
  - `is_default`: Boolean (default: false)
  - `created_at`: Datetime
  - `updated_at`: Datetime

### Task
- **Purpose**: Individual tasks within todos
- **Attributes**:
  - `id`: Integer (Primary Key)
  - `todo_id`: Integer (Foreign Key to Todo)
  - `user_id`: Integer (Foreign Key to User)
  - `title`: String, Required
  - `description`: String, Optional
  - `priority`: Enum (LOW, MEDIUM, HIGH, URGENT), default: MEDIUM
  - `status`: Enum (TODO, IN_PROGRESS, COMPLETED, BLOCKED), default: TODO
  - `due_date`: Date, Optional
  - `completed_at`: Datetime, Optional
  - `created_at`: Datetime
  - `updated_at`: Datetime

---

## User Stories

### US1: User Authentication
**Goal**: Secure user registration and login with JWT token generation

**Acceptance Criteria**:
- [x] User can register with email and password
- [x] Password is securely hashed with bcrypt (72-byte limit)
- [x] User can login with email and password
- [x] Valid credentials return JWT token with 30-minute expiry
- [x] Invalid credentials return 401 error
- [x] JWT contains user email in 'sub' claim
- [x] Logout endpoint clears authentication

**Independent Test**: User can register, login, receive token, and logout successfully

---

### US2: User Profile Management
**Goal**: Users can view and update their profile information

**Acceptance Criteria**:
- [ ] GET /api/auth/me returns authenticated user profile
- [ ] User can only access their own profile data
- [ ] User can update their name and email
- [ ] Email uniqueness is enforced during updates
- [ ] Profile updates return updated user object
- [ ] Unauthorized requests return 401

**Independent Test**: Authenticated user can view and update profile without accessing other users' data

---

### US3: Todo Management
**Goal**: Users can create, read, update, and delete todo lists

**Acceptance Criteria**:
- [ ] GET /api/todos returns user's todos with pagination
- [ ] POST /api/todos creates new todo for authenticated user
- [ ] GET /api/todos/{id} returns single todo
- [ ] PUT /api/todos/{id} updates todo properties
- [ ] DELETE /api/todos/{id} removes todo and associated tasks
- [ ] Each todo is filtered by user_id (no cross-user access)
- [ ] Title is required; description and color are optional

**Independent Test**: User can create, view, update, and delete todos with proper data isolation

---

### US4: Task Management (CRUD)
**Goal**: Users can create, read, update, and delete tasks within todos

**Acceptance Criteria**:
- [ ] GET /api/tasks returns user's tasks with filters (todo_id, status, priority)
- [ ] POST /api/tasks creates new task with required title and optional properties
- [ ] GET /api/tasks/{id} returns single task
- [ ] PUT /api/tasks/{id} updates task properties (title, description, priority, status, due_date)
- [ ] DELETE /api/tasks/{id} removes task
- [ ] Tasks are filtered by user_id (no cross-user access)
- [ ] Completing task sets completed_at timestamp
- [ ] Invalid status/priority values return validation error

**Independent Test**: User can perform full CRUD on tasks with proper filtering and validation

---

### US5: Task Status Management
**Goal**: Users can track task progress with status and completion

**Acceptance Criteria**:
- [ ] Task status can be: TODO, IN_PROGRESS, COMPLETED, BLOCKED
- [ ] Changing status to COMPLETED sets completed_at timestamp
- [ ] Changing status from COMPLETED clears completed_at timestamp
- [ ] Completion percentage calculated from completed tasks in todo
- [ ] Status changes return updated task object

**Independent Test**: Task status transitions work correctly with timestamp management

---

### US6: Dashboard Analytics
**Goal**: Provide user dashboard with task statistics and overview

**Acceptance Criteria**:
- [ ] GET /api/dashboard returns aggregated statistics for authenticated user
- [ ] Statistics include:
  - Total tasks count
  - Completed tasks count
  - In-progress tasks count
  - Blocked tasks count
  - Completion percentage
  - Tasks by priority (LOW, MEDIUM, HIGH, URGENT)
  - Tasks due today
  - Overdue tasks
- [ ] Statistics filtered by user_id
- [ ] Response includes recent tasks (last 5)

**Independent Test**: Dashboard endpoint returns accurate statistics without exposing other users' data

---

### US7: Task Filtering & Search
**Goal**: Users can filter and search tasks efficiently

**Acceptance Criteria**:
- [ ] GET /api/tasks supports query parameters:
  - `todo_id`: Filter by specific todo
  - `status`: Filter by status
  - `priority`: Filter by priority
  - `due_date`: Filter by due date range
  - `search`: Full-text search in title and description
  - `sort`: Sort by created_at, due_date, or priority
  - `limit` and `offset`: Pagination
- [ ] Filters work in combination
- [ ] Results sorted correctly
- [ ] Pagination returns correct subset with total count

**Independent Test**: Filtering and searching works with various combinations of parameters

---

## API Endpoints

### Authentication Endpoints

#### POST /api/auth/register
- **Request**: `{ email, password, name }`
- **Response**: `{ user: {id, email, name}, token }`
- **Errors**: 400 (email exists), 422 (validation)
- **Status**: ✅ IMPLEMENTED

#### POST /api/auth/login
- **Request**: `{ email, password }`
- **Response**: `{ user: {id, email, name}, token }`
- **Errors**: 401 (invalid credentials)
- **Status**: ✅ IMPLEMENTED

#### POST /api/auth/logout
- **Response**: `{ message: "Logged out successfully" }`
- **Requires**: JWT Token
- **Status**: ✅ IMPLEMENTED

#### GET /api/auth/me
- **Response**: `{ id, email, name, created_at }`
- **Requires**: JWT Token
- **Errors**: 401 (invalid/missing token)
- **Status**: ✅ IMPLEMENTED

---

### Todo Endpoints

#### GET /api/todos
- **Query**: `?skip=0&limit=10`
- **Response**: `[ { id, title, description, color, created_at, task_count, completed_count } ]`
- **Requires**: JWT Token
- **Status**: 🔴 NOT IMPLEMENTED

#### POST /api/todos
- **Request**: `{ title, description?, color? }`
- **Response**: `{ id, title, description, color, created_at }`
- **Requires**: JWT Token
- **Status**: 🔴 NOT IMPLEMENTED

#### GET /api/todos/{id}
- **Response**: `{ id, title, description, color, created_at, tasks: [...] }`
- **Requires**: JWT Token, ownership
- **Status**: 🔴 NOT IMPLEMENTED

#### PUT /api/todos/{id}
- **Request**: `{ title?, description?, color? }`
- **Response**: `{ id, title, description, color }`
- **Requires**: JWT Token, ownership
- **Status**: 🔴 NOT IMPLEMENTED

#### DELETE /api/todos/{id}
- **Response**: `{ message: "Todo deleted" }`
- **Requires**: JWT Token, ownership
- **Status**: 🔴 NOT IMPLEMENTED

---

### Task Endpoints

#### GET /api/tasks
- **Query**: `?todo_id=123&status=TODO&priority=HIGH&skip=0&limit=20`
- **Response**: `[ { id, title, description, priority, status, due_date, completed_at, created_at } ]`
- **Requires**: JWT Token
- **Status**: 🔴 NOT IMPLEMENTED

#### POST /api/tasks
- **Request**: `{ todo_id, title, description?, priority?, due_date? }`
- **Response**: `{ id, title, description, priority, status, due_date, created_at }`
- **Requires**: JWT Token
- **Status**: 🔴 NOT IMPLEMENTED

#### GET /api/tasks/{id}
- **Response**: `{ id, title, description, priority, status, due_date, completed_at, created_at }`
- **Requires**: JWT Token, ownership
- **Status**: 🔴 NOT IMPLEMENTED

#### PUT /api/tasks/{id}
- **Request**: `{ title?, description?, priority?, status?, due_date? }`
- **Response**: `{ id, title, description, priority, status, due_date, completed_at }`
- **Requires**: JWT Token, ownership
- **Status**: 🔴 NOT IMPLEMENTED

#### DELETE /api/tasks/{id}
- **Response**: `{ message: "Task deleted" }`
- **Requires**: JWT Token, ownership
- **Status**: 🔴 NOT IMPLEMENTED

---

### Dashboard Endpoints

#### GET /api/dashboard
- **Response**: 
```json
{
  "stats": {
    "total_tasks": 12,
    "completed_tasks": 5,
    "in_progress_tasks": 4,
    "blocked_tasks": 1,
    "completion_percentage": 42,
    "by_priority": { "LOW": 3, "MEDIUM": 5, "HIGH": 3, "URGENT": 1 },
    "due_today": 2,
    "overdue": 1
  },
  "recent_tasks": [...]
}
```
- **Requires**: JWT Token
- **Status**: 🔴 NOT IMPLEMENTED

---

## Authentication & Security

### JWT Token Format
```json
{
  "sub": "user@example.com",
  "exp": 1704067200,
  "iat": 1704063600
}
```

### Authorization Rules
1. All endpoints except `/api/auth/register` and `/api/auth/login` require valid JWT
2. JWT verified using BETTER_AUTH_SECRET
3. Token expiry: 30 minutes
4. User identity derived from JWT `sub` claim
5. All database queries filtered by authenticated user_id
6. Unauthorized requests return 401
7. Cross-user access attempts return 403

### Password Requirements
- Minimum 8 characters
- Bcrypt hashing with 12 rounds
- Password truncated to 72 bytes before hashing (bcrypt limit)
- Never stored in plaintext

---

## Error Handling

### Standard Error Responses

**400 Bad Request**
```json
{ "detail": "Invalid request data" }
```

**401 Unauthorized**
```json
{ "detail": "Invalid or missing token" }
```

**403 Forbidden**
```json
{ "detail": "Access denied" }
```

**404 Not Found**
```json
{ "detail": "Resource not found" }
```

**422 Unprocessable Entity**
```json
{ "detail": [{ "type": "...", "loc": [...], "msg": "..." }] }
```

**500 Internal Server Error**
```json
{ "detail": "Internal server error" }
```

---

## Data Validation

### Email
- Must be valid email format
- Unique across users
- Case-insensitive comparison

### Password
- Minimum 8 characters
- Maximum 72 bytes (bcrypt limit)
- No specific character requirements

### Title Fields
- Required, non-empty
- Maximum 255 characters
- Trimmed of whitespace

### Descriptions
- Optional
- Maximum 2000 characters

### Priority
- Must be one of: LOW, MEDIUM, HIGH, URGENT
- Case-sensitive

### Status
- Must be one of: TODO, IN_PROGRESS, COMPLETED, BLOCKED
- Case-sensitive

### Due Date
- Valid ISO 8601 date format (YYYY-MM-DD)
- Optional
- Can be in the past (for overdue tracking)

---

## Performance Considerations

- Pagination default: 10 items
- Pagination maximum: 100 items
- Database indexes on: user_id, todo_id, status, priority
- Response times: < 200ms for most endpoints
- Connection pooling: 20-50 connections

---

## Testing Requirements

All endpoints must have:
- Unit tests for business logic
- Integration tests for database operations
- API tests for request/response validation
- Security tests for authentication/authorization
- Error case tests for all error scenarios

---

## Deployment Notes

- Environment: Neon Serverless PostgreSQL
- API hosted on dedicated server (port 8001)
- CORS enabled for frontend origin
- Health check endpoint: GET /health
- Database migrations handled via SQLAlchemy
