from sqlmodel import Session, select, func
from typing import List, Optional
from ..models.task import Task


def create_task(session: Session, task: Task) -> Task:
    """
    Create a new task in the database.

    Args:
        session: Database session
        task: Task object to create

    Returns:
        Created task object
    """
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task_by_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Get a task by its ID for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user who owns the task

    Returns:
        Task object if found and owned by user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    return session.exec(statement).first()


def get_tasks_for_user(
    session: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    completed: Optional[bool] = None
) -> List[Task]:
    """
    Get a list of tasks for a specific user with optional filters.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        completed: Filter by completion status (optional)

    Returns:
        List of Task objects
    """
    query = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())

    return session.exec(query).all()


def update_task(session: Session, task_id: int, user_id: int, update_data: dict) -> Optional[Task]:
    """
    Update a task for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user who owns the task
        update_data: Dictionary of fields to update

    Returns:
        Updated Task object if successful, None if not found or not owned by user
    """
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        return None

    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    """
    Delete a task for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user who owns the task

    Returns:
        True if deletion was successful, False if task not found or not owned by user
    """
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        return False

    session.delete(task)
    session.commit()

    return True


def toggle_task_completion(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Toggle the completion status of a task for a specific user.

    Args:
        session: Database session
        task_id: ID of the task to toggle
        user_id: ID of the user who owns the task

    Returns:
        Updated Task object if successful, None if not found or not owned by user
    """
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        return None

    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def get_task_count_for_user(session: Session, user_id: int, completed: Optional[bool] = None) -> int:
    """
    Get the count of tasks for a specific user with optional filter.

    Args:
        session: Database session
        user_id: ID of the user whose task count to retrieve
        completed: Filter by completion status (optional)

    Returns:
        Number of tasks matching the criteria
    """
    query = select(func.count(Task.id)).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    return session.exec(query).one()