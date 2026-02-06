# Backend Implementation Tasks

**Project**: Premium Todo Application | **Component**: Backend API
**Spec Reference**: [specs/backend/spec.md](spec.md) | **Plan Reference**: [specs/backend/plan.md](plan.md)

## Phase 1: Core Infrastructure (Models, Services, Schema)

### Phase 1.1: Database Models

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T1.1.1 | Create Todo SQLModel with all fields | `[ ]` | 15min | Fields: id, user_id, title, description, created_at, updated_at. Add indexes on user_id and created_at |
| T1.1.2 | Create Task SQLModel with relationships | `[ ]` | 20min | Fields: id, todo_id, user_id, title, description, status, priority, due_date, completed_at, created_at, updated_at. Add foreign key to todo_id |
| T1.1.3 | Add database migration for new models | `[ ]` | 15min | Create migration file, test migration up/down |
| T1.1.4 | Verify models work with SQLModel session | `[ ]` | 10min | Test create/read operations |

**Phase 1.1 Output**: Todo and Task models fully integrated with database

---

### Phase 1.2: Request/Response Schemas

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T1.2.1 | Create Pydantic schemas for Todo | `[ ]` | 15min | TodoCreate, TodoUpdate, TodoResponse, TodoListResponse |
| T1.2.2 | Create Pydantic schemas for Task | `[ ]` | 20min | TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, TaskFilterResponse |
| T1.2.3 | Create Dashboard response schema | `[ ]` | 15min | DashboardStats, TaskBreakdown, RecentTask, DashboardResponse |
| T1.2.4 | Add validation to all schemas | `[ ]` | 15min | Email, URL, length constraints, enum validation |

**Phase 1.2 Output**: All request/response schemas documented and validated

---

### Phase 1.3: Service Layer

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T1.3.1 | Create TodoService class with methods | `[ ]` | 30min | Methods: create_todo, get_todo, get_todos, update_todo, delete_todo, get_task_count |
| T1.3.2 | Create TaskService class with methods | `[ ]` | 40min | Methods: create_task, get_task, get_tasks (with filters), update_task, delete_task, update_status |
| T1.3.3 | Create DashboardService class | `[ ]` | 30min | Methods: get_statistics, calculate_completion, get_priority_breakdown, get_recent_tasks, get_overdue_tasks |
| T1.3.4 | Implement user data isolation in services | `[ ]` | 20min | All queries filtered by user_id to prevent cross-user access |
| T1.3.5 | Add error handling and validation in services | `[ ]` | 20min | ValueError, NotFoundError, UnauthorizedError |

**Phase 1.3 Output**: All business logic encapsulated in services

---

### Phase 1.4: Error Handling & Logging

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T1.4.1 | Add global exception handlers to FastAPI app | `[ ]` | 20min | Handle HTTPException, ValueError, database errors |
| T1.4.2 | Implement error response schema | `[ ]` | 10min | Standard format: {error, message, details} |
| T1.4.3 | Add request/response logging middleware | `[ ]` | 15min | Log endpoint, method, status, response time |
| T1.4.4 | Configure logging for services | `[ ]` | 15min | Add logging for important operations and errors |

**Phase 1.4 Output**: Comprehensive error handling and observability

---

## Phase 2: Todo Management CRUD

### Phase 2.1: Todo Endpoints - List & Create

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T2.1.1 | Implement GET /api/todos endpoint | `[ ]` | 15min | Return list of user's todos with pagination (skip, limit). Include task counts. |
| T2.1.2 | Implement POST /api/todos endpoint | `[ ]` | 15min | Create new todo. Validate title (required, 1-255 chars). Return created todo with id. |
| T2.1.3 | Add pagination to todo list response | `[ ]` | 10min | Support skip and limit parameters. Return total count. |
| T2.1.4 | Test CREATE and LIST operations | `[ ]` | 15min | Test valid inputs, validation errors, user isolation |

**Phase 2.1 Output**: Users can list and create todos

---

### Phase 2.2: Todo Endpoints - Read, Update, Delete

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T2.2.1 | Implement GET /api/todos/{id} endpoint | `[ ]` | 15min | Return single todo with task count. Return 404 if not found or not authorized. |
| T2.2.2 | Implement PUT /api/todos/{id} endpoint | `[ ]` | 15min | Update todo title/description. Validate inputs. Return updated todo. |
| T2.2.3 | Implement DELETE /api/todos/{id} endpoint | `[ ]` | 15min | Delete todo and cascade delete all tasks. Return 204 No Content. |
| T2.2.4 | Add 403 Unauthorized handling | `[ ]` | 10min | Return 403 when accessing other users' todos |
| T2.2.5 | Test READ, UPDATE, DELETE operations | `[ ]` | 20min | Test all CRUD flows, error cases, authorization |

**Phase 2.2 Output**: Complete Todo CRUD working with authorization

---

### Phase 2.3: Todo Integration Testing

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T2.3.1 | Write integration tests for all todo endpoints | `[ ]` | 30min | Test all CRUD operations with real database |
| T2.3.2 | Test user isolation (no cross-user access) | `[ ]` | 15min | Verify 403 returned when accessing other users' todos |
| T2.3.3 | Test validation errors | `[ ]` | 15min | Test invalid inputs (empty title, missing user, etc.) |
| T2.3.4 | Test pagination | `[ ]` | 10min | Test skip/limit parameters work correctly |

**Phase 2.3 Output**: All todo endpoints tested and verified

---

## Phase 3: Task Management CRUD

### Phase 3.1: Task Endpoints - List & Create

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T3.1.1 | Implement GET /api/tasks endpoint | `[ ]` | 20min | Return list of user's tasks. Support filtering by todo_id, status, priority. Include pagination. |
| T3.1.2 | Implement POST /api/tasks endpoint | `[ ]` | 20min | Create new task. Validate required fields (title, todo_id). Set status to TODO. Return created task. |
| T3.1.3 | Add task filtering by todo_id | `[ ]` | 10min | Support query parameter ?todo_id=X to filter tasks |
| T3.1.4 | Test task creation and listing | `[ ]` | 15min | Test valid inputs, validation, filtering |

**Phase 3.1 Output**: Users can list and create tasks with basic filtering

---

### Phase 3.2: Task Endpoints - Read, Update, Delete

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T3.2.1 | Implement GET /api/tasks/{id} endpoint | `[ ]` | 15min | Return single task. Return 404 if not found. |
| T3.2.2 | Implement PUT /api/tasks/{id} endpoint | `[ ]` | 20min | Update task properties. Validate status and priority enums. Handle completed_at timestamp. |
| T3.2.3 | Implement DELETE /api/tasks/{id} endpoint | `[ ]` | 15min | Delete task. Return 204 No Content. |
| T3.2.4 | Add status transition logic | `[ ]` | 15min | When status changes to COMPLETED, set completed_at. When reverted, clear completed_at. |
| T3.2.5 | Test READ, UPDATE, DELETE operations | `[ ]` | 20min | Test all CRUD flows, status transitions, error cases |

**Phase 3.2 Output**: Complete Task CRUD with status management

---

### Phase 3.3: Task Integration Testing

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T3.3.1 | Write integration tests for all task endpoints | `[ ]` | 30min | Test all CRUD operations with real database |
| T3.3.2 | Test status transition logic | `[ ]` | 15min | Test completed_at timestamp management |
| T3.3.3 | Test cross-user isolation | `[ ]` | 15min | Verify users can't access other users' tasks |
| T3.3.4 | Test validation (status, priority enums) | `[ ]` | 15min | Test invalid status/priority values rejected |

**Phase 3.3 Output**: All task endpoints tested with status management verified

---

## Phase 4: Advanced Filtering & Searching

### Phase 4.1: Task Filtering

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T4.1.1 | Add status filtering to GET /api/tasks | `[ ]` | 15min | Support ?status=TODO,IN_PROGRESS,COMPLETED,BLOCKED (comma-separated) |
| T4.1.2 | Add priority filtering | `[ ]` | 10min | Support ?priority=LOW,MEDIUM,HIGH,URGENT |
| T4.1.3 | Add due_date range filtering | `[ ]` | 15min | Support ?due_date_from=YYYY-MM-DD&due_date_to=YYYY-MM-DD |
| T4.1.4 | Implement full-text search on title/description | `[ ]` | 15min | Support ?search=keyword to search title and description |

**Phase 4.1 Output**: Advanced filtering capabilities working

---

### Phase 4.2: Task Sorting & Pagination

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T4.2.1 | Add sorting to task list | `[ ]` | 15min | Support ?sort_by=created_at,due_date,priority and ?sort_order=asc,desc |
| T4.2.2 | Implement pagination with total count | `[ ]` | 10min | Return total count in response header or body |
| T4.2.3 | Test complex filter combinations | `[ ]` | 20min | Test status + priority + due_date filters together |
| T4.2.4 | Validate all filter parameters | `[ ]` | 10min | Return 422 for invalid filter values |

**Phase 4.2 Output**: Complete filtering, sorting, and pagination system

---

## Phase 5: Dashboard Analytics

### Phase 5.1: Dashboard Endpoint

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T5.1.1 | Implement GET /api/dashboard endpoint | `[ ]` | 20min | Return all statistics required by spec |
| T5.1.2 | Calculate completion statistics | `[ ]` | 15min | Total tasks, completed tasks, completion percentage |
| T5.1.3 | Break down tasks by priority | `[ ]` | 15min | Count of HIGH, MEDIUM, LOW, URGENT priority tasks |
| T5.1.4 | Identify due-today tasks | `[ ]` | 10min | Return tasks with due_date = today |
| T5.1.5 | Identify overdue tasks | `[ ]` | 10min | Return tasks with due_date < today and status != COMPLETED |

**Phase 5.1 Output**: Dashboard endpoint fully functional with all statistics

---

### Phase 5.2: Dashboard Response & Testing

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T5.2.1 | Format dashboard response | `[ ]` | 10min | Structure response according to spec |
| T5.2.2 | Get recent tasks (last 5 created) | `[ ]` | 10min | Include in dashboard response |
| T5.2.3 | Test dashboard calculations | `[ ]` | 20min | Verify statistics accuracy with test data |
| T5.2.4 | Test dashboard with no tasks | `[ ]` | 10min | Return zeros/empty lists appropriately |

**Phase 5.2 Output**: Dashboard working with accurate statistics

---

## Phase 6: User Profile Management

### Phase 6.1: User Profile Endpoints

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T6.1.1 | Implement GET /api/auth/me endpoint (enhance) | `[ ]` | 10min | Already implemented, ensure returns all user fields |
| T6.1.2 | Implement PUT /api/auth/profile endpoint | `[ ]` | 15min | Update name and email. Validate email uniqueness. |
| T6.1.3 | Add email uniqueness validation | `[ ]` | 10min | Check email not used by other users |
| T6.1.4 | Test profile update operations | `[ ]` | 15min | Test valid updates, validation, email uniqueness |

**Phase 6.1 Output**: User profile management complete

---

## Phase 7: Comprehensive Testing

### Phase 7.1: Unit Tests

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T7.1.1 | Unit test TodoService | `[ ]` | 20min | Test all methods with mocked database |
| T7.1.2 | Unit test TaskService | `[ ]` | 25min | Test all methods, filtering logic, status transitions |
| T7.1.3 | Unit test DashboardService | `[ ]` | 15min | Test statistics calculations with mock data |
| T7.1.4 | Unit test validation schemas | `[ ]` | 15min | Test all Pydantic model validations |

**Phase 7.1 Output**: All services have unit test coverage

---

### Phase 7.2: Integration Tests

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T7.2.1 | End-to-end test: signup → create todo → create task → update status | `[ ]` | 30min | Test complete user flow |
| T7.2.2 | Integration test: cross-user isolation | `[ ]` | 20min | Test two users can't access each other's data |
| T7.2.3 | Integration test: error scenarios | `[ ]` | 20min | Test 404, 403, 422, 500 errors |
| T7.2.4 | Integration test: filtering and pagination | `[ ]` | 20min | Test all filter combinations |

**Phase 7.2 Output**: Complete integration test suite passing

---

### Phase 7.3: Documentation

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T7.3.1 | Create API documentation with examples | `[ ]` | 30min | Document all endpoints with request/response examples |
| T7.3.2 | Add Swagger/OpenAPI spec | `[ ]` | 20min | Enable /docs endpoint with full API documentation |
| T7.3.3 | Document error responses | `[ ]` | 15min | Document all possible error codes and meanings |
| T7.3.4 | Create deployment guide | `[ ]` | 20min | Document how to deploy backend |

**Phase 7.3 Output**: Complete API documentation

---

## Phase 8: Security & Performance

### Phase 8.1: Security Hardening

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T8.1.1 | Implement rate limiting on auth endpoints | `[ ]` | 20min | Limit login/register attempts to prevent brute force |
| T8.1.2 | Add request size limits | `[ ]` | 10min | Prevent large payloads |
| T8.1.3 | Implement CORS properly | `[ ]` | 10min | Allow frontend origin, restrict others |
| T8.1.4 | Audit response data | `[ ]` | 15min | Ensure no sensitive data (passwords, tokens) in responses |
| T8.1.5 | Test security headers | `[ ]` | 10min | Add X-Content-Type-Options, X-Frame-Options, etc. |

**Phase 8.1 Output**: Backend hardened against common vulnerabilities

---

### Phase 8.2: Performance Optimization

| # | Task | Status | Time | Details |
|---|------|--------|------|---------|
| T8.2.1 | Implement database connection pooling | `[ ]` | 15min | Configure SQLAlchemy pool size (20-50 connections) |
| T8.2.2 | Add query optimization | `[ ]` | 20min | Use eager loading, avoid N+1 queries |
| T8.2.3 | Performance test endpoints | `[ ]` | 20min | Measure response times, ensure < 200ms for basic ops |
| T8.2.4 | Add caching for dashboard | `[ ]` | 15min | Cache statistics for 1 minute to reduce database load |
| T8.2.5 | Profile slow endpoints | `[ ]` | 15min | Identify and optimize bottlenecks |

**Phase 8.2 Output**: Backend optimized for performance

---

## Task Dependency Graph

```
Phase 1 (Infrastructure)
├── T1.1 (Models) → T1.2 (Schemas) → T1.3 (Services) → T1.4 (Error Handling)
│
Phase 2 (Todo CRUD)
├── T2.1 (Create/List) → T2.2 (Read/Update/Delete) → T2.3 (Testing)
│
Phase 3 (Task CRUD)
├── T3.1 (Create/List) → T3.2 (Read/Update/Delete) → T3.3 (Testing)
│
Phase 4 (Advanced Filtering)
├── T4.1 (Filtering) → T4.2 (Sorting/Pagination)
│
Phase 5 (Dashboard)
├── T5.1 (Endpoint) → T5.2 (Testing)
│
Phase 6 (User Profile)
├── T6.1 (Endpoints)
│
Phase 7 (Testing & Docs)
├── T7.1 (Unit Tests) & T7.2 (Integration Tests) & T7.3 (Documentation)
│
Phase 8 (Security & Performance)
├── T8.1 (Security) & T8.2 (Performance)
```

**Critical Path** (minimum to MVP):
Phase 1 → Phase 2 → Phase 3 → Phase 7 (Core Testing)

**Recommended Path** (feature-complete):
All phases in order (1-8)

---

## Execution Checklist

### Pre-Implementation
- [ ] Database connection verified
- [ ] Authentication endpoints working
- [ ] Development environment setup
- [ ] All dependencies installed

### Phase 1 Validation
- [ ] Models created in `backend/models/`
- [ ] Services created in `backend/services/`
- [ ] Error handling implemented
- [ ] All imports working

### Phase 2 Validation
- [ ] Todo endpoints registered in FastAPI
- [ ] All todo CRUD operations working
- [ ] Tests passing for todo endpoints
- [ ] User isolation verified

### Phase 3 Validation
- [ ] Task endpoints registered
- [ ] All task CRUD operations working
- [ ] Status transitions correct
- [ ] Tests passing

### Phase 4 Validation
- [ ] Filtering parameters working
- [ ] Sorting parameters working
- [ ] Search functionality working
- [ ] Complex filters work together

### Phase 5 Validation
- [ ] Dashboard endpoint returns correct data
- [ ] Statistics calculations verified
- [ ] Recent tasks included
- [ ] Overdue/due-today identification correct

### Phase 6 Validation
- [ ] Profile endpoints working
- [ ] Email uniqueness enforced
- [ ] Updates reflected in database

### Phase 7 Validation
- [ ] All tests passing
- [ ] Coverage > 80%
- [ ] API documentation complete
- [ ] Swagger docs accessible

### Phase 8 Validation
- [ ] Security headers present
- [ ] Rate limiting working
- [ ] Response times acceptable
- [ ] No sensitive data in responses

---

## Notes

- Tasks marked with `[ ]` are not started. Update to `[x]` as they complete.
- Each task includes time estimate. Adjust based on actual experience.
- Maintain backwards compatibility during implementation.
- Document decisions in commit messages.
- Test as you go, don't leave testing to the end.
