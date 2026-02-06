"""
Task Service - Handles business logic for task operations
"""
from sqlmodel import Session, select, func, and_, or_
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models.task import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from typing import Optional


class TaskService:
    """Service class for task operations"""

    @staticmethod
    def create_task(session: Session, user_id: int, task_create: TaskCreate) -> Task:
        """Create a new task for the user"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Log the incoming data
            logger.info(f"Creating task for user {user_id}: title={task_create.title}, todo_id={task_create.todo_id}")
            
            # Verify todo_id exists if provided
            if task_create.todo_id:
                from models.todo import Todo
                todo = session.query(Todo).filter(
                    Todo.id == task_create.todo_id,
                    Todo.user_id == user_id
                ).first()
                if not todo:
                    logger.error(f"Todo {task_create.todo_id} not found for user {user_id}")
                    raise HTTPException(status_code=404, detail="Todo not found")
            
            task = Task(
                user_id=user_id,
                todo_id=task_create.todo_id if task_create.todo_id else None,
                title=task_create.title,
                description=task_create.description,
                status=task_create.status,
                priority=task_create.priority,
                due_date=task_create.due_date,
            )
            logger.info(f"Task object created: {task}")
            
            session.add(task)
            session.commit()
            session.refresh(task)
            logger.info(f"Task created successfully: {task.id}")
            return task
        except HTTPException:
            session.rollback()
            raise
        except IntegrityError as e:
            session.rollback()
            logger.error(f"IntegrityError creating task: {str(e.orig)}")
            # Provide a clearer error message for common integrity issues
            raise HTTPException(status_code=400, detail=f"Invalid data: {str(e.orig)}")
        except Exception as e:
            session.rollback()
            logger.error(f"Unexpected error creating task: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

    @staticmethod
    def get_task(session: Session, user_id: int, task_id: int) -> Optional[Task]:
        """Get a single task by ID, ensuring user ownership"""
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def get_tasks(
        session: Session,
        user_id: int,
        todo_id: Optional[int] = None,
        status: Optional[list[TaskStatus]] = None,
        priority: Optional[list[TaskPriority]] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[Task], int]:
        """Get tasks with advanced filtering"""
        # Base filter: user ownership
        filters = [Task.user_id == user_id]

        # Add optional filters
        if todo_id is not None:
            filters.append(Task.todo_id == todo_id)

        if status:
            filters.append(Task.status.in_(status))

        if priority:
            filters.append(Task.priority.in_(priority))

        if due_date_from:
            filters.append(Task.due_date >= due_date_from)

        if due_date_to:
            filters.append(Task.due_date <= due_date_to)

        if search:
            search_filter = or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
            filters.append(search_filter)

        # Get total count
        count_statement = select(func.count(Task.id)).where(and_(*filters))
        total = session.exec(count_statement).one()

        # Build query with sorting
        statement = select(Task).where(and_(*filters))

        # Add sorting
        if sort_by == "created_at":
            statement = statement.order_by(
                Task.created_at.desc() if sort_order == "desc" else Task.created_at.asc()
            )
        elif sort_by == "due_date":
            statement = statement.order_by(
                Task.due_date.desc() if sort_order == "desc" else Task.due_date.asc()
            )
        elif sort_by == "priority":
            statement = statement.order_by(
                Task.priority.desc() if sort_order == "desc" else Task.priority.asc()
            )
        else:
            statement = statement.order_by(
                Task.created_at.desc() if sort_order == "desc" else Task.created_at.asc()
            )

        # Add pagination
        statement = statement.offset(skip).limit(limit)

        tasks = session.exec(statement).all()
        return tasks, total

    @staticmethod
    def update_task(session: Session, user_id: int, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task, ensuring user ownership"""
        task = TaskService.get_task(session, user_id, task_id)
        if not task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)

        # Handle status change - set completed_at when status changes to COMPLETED
        if "status" in update_data:
            new_status = update_data["status"]
            if new_status == TaskStatus.COMPLETED:
                if task.completed_at is None:
                    task.completed_at = datetime.utcnow()
            elif task.completed_at is not None:
                # If status reverted from COMPLETED, clear completed_at
                task.completed_at = None

        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, user_id: int, task_id: int) -> bool:
        """Delete a task, ensuring user ownership"""
        task = TaskService.get_task(session, user_id, task_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def get_task_counts_by_status(session: Session, user_id: int) -> dict[str, int]:
        """Get count of tasks by status for a user"""
        statement = select(Task.status, func.count(Task.id)).where(
            Task.user_id == user_id
        ).group_by(Task.status)

        results = session.exec(statement).all()
        counts = {
            TaskStatus.TODO: 0,
            TaskStatus.IN_PROGRESS: 0,
            TaskStatus.COMPLETED: 0,
            TaskStatus.BLOCKED: 0,
        }

        for status, count in results:
            counts[status] = count

        return counts

    @staticmethod
    def get_task_counts_by_priority(session: Session, user_id: int) -> dict[str, int]:
        """Get count of tasks by priority for a user"""
        statement = select(Task.priority, func.count(Task.id)).where(
            Task.user_id == user_id
        ).group_by(Task.priority)

        results = session.exec(statement).all()
        counts = {
            TaskPriority.LOW: 0,
            TaskPriority.MEDIUM: 0,
            TaskPriority.HIGH: 0,
            TaskPriority.URGENT: 0,
        }

        for priority, count in results:
            counts[priority] = count

        return counts