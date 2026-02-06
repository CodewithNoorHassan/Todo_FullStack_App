from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional

from database.session import get_session
from models.task import Task, TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from auth.jwt_handler import get_current_user
from models.user import User
from services.task_service import TaskService


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=500),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    todo_id: Optional[int] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc")
):
    """
    Get a list of tasks for the authenticated user.

    Args:
        current_user: The authenticated user
        session: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        completed: Filter by completion status (optional)

    Returns:
        List of tasks for the user
    """
    # parse comma-separated enums into lists if present
    status_list = status.split(",") if status else None
    priority_list = priority.split(",") if priority else None

    tasks, total = TaskService.get_tasks(
        session,
        current_user.id,
        todo_id=todo_id,
        status=status_list,
        priority=priority_list,
        search=search,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return {"tasks": tasks, "total": total, "skip": skip, "limit": limit}


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_create: Task creation data
        current_user: The authenticated user
        session: Database session

    Returns:
        The created task
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"POST /api/tasks - User {current_user.id} creating task: {task_create}")
    
    try:
        new_task = TaskService.create_task(session, current_user.id, task_create)
        logger.info(f"Task created successfully: {new_task.id}")
        return new_task
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}", exc_info=True)
        raise


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.

    Args:
        task_id: The ID of the task to retrieve
        current_user: The authenticated user
        session: Database session

    Returns:
        The requested task

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    t = TaskService.get_task(session, current_user.id, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the authenticated user.

    Args:
        task_id: The ID of the task to update
        task_update: Task update data
        current_user: The authenticated user
        session: Database session

    Returns:
        The updated task

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    updated = TaskService.update_task(session, current_user.id, task_id, task_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the authenticated user.

    Args:
        task_id: The ID of the task to delete
        current_user: The authenticated user
        session: Database session

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    deleted = TaskService.delete_task(session, current_user.id, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/toggle")
async def toggle_task_completion(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user.

    Args:
        task_id: The ID of the task to toggle
        current_user: The authenticated user
        session: Database session

    Returns:
        The updated task

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    # Fetch current task
    task_obj = TaskService.get_task(session, current_user.id, task_id)
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")

    # Toggle completion status using TaskStatus enum
    from models.task import TaskUpdate as TaskUpdateModel, TaskStatus

    toggle = TaskUpdateModel()
    toggle.status = TaskStatus.TODO if task_obj.status == TaskStatus.COMPLETED else TaskStatus.COMPLETED

    updated = TaskService.update_task(session, current_user.id, task_id, toggle)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated