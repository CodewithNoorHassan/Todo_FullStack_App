"""
Todo Service - Handles business logic for todo operations
"""
from sqlmodel import Session, select, func
from datetime import datetime
from models.todo import Todo, TodoCreate, TodoUpdate
from models.task import Task


class TodoService:
    """Service class for todo operations"""

    @staticmethod
    def create_todo(session: Session, user_id: int, todo_create: TodoCreate) -> Todo:
        """Create a new todo for the user"""
        todo = Todo(
            user_id=user_id,
            title=todo_create.title,
            description=todo_create.description,
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def get_todo(session: Session, user_id: int, todo_id: int) -> Todo | None:
        """Get a single todo by ID, ensuring user ownership"""
        statement = select(Todo).where(
            Todo.id == todo_id,
            Todo.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def get_todos(session: Session, user_id: int, skip: int = 0, limit: int = 50) -> tuple[list[Todo], int]:
        """Get all todos for a user with pagination"""
        # Get total count
        count_statement = select(func.count(Todo.id)).where(Todo.user_id == user_id)
        total = session.exec(count_statement).one()

        # Get paginated results
        statement = (
            select(Todo)
            .where(Todo.user_id == user_id)
            .order_by(Todo.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        todos = session.exec(statement).all()
        return todos, total

    @staticmethod
    def update_todo(session: Session, user_id: int, todo_id: int, todo_update: TodoUpdate) -> Todo | None:
        """Update a todo, ensuring user ownership"""
        todo = TodoService.get_todo(session, user_id, todo_id)
        if not todo:
            return None

        update_data = todo_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo, key, value)
        todo.updated_at = datetime.utcnow()

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def delete_todo(session: Session, user_id: int, todo_id: int) -> bool:
        """Delete a todo and all its tasks, ensuring user ownership"""
        todo = TodoService.get_todo(session, user_id, todo_id)
        if not todo:
            return False

        # Delete all tasks associated with this todo
        statement = select(Task).where(Task.todo_id == todo_id)
        tasks = session.exec(statement).all()
        for task in tasks:
            session.delete(task)

        session.delete(todo)
        session.commit()
        return True

    @staticmethod
    def get_task_count(session: Session, todo_id: int) -> int:
        """Get the number of tasks in a todo"""
        statement = select(func.count(Task.id)).where(Task.todo_id == todo_id)
        return session.exec(statement).one()
