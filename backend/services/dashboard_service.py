"""
Dashboard Service - Handles business logic for dashboard analytics
"""
from sqlmodel import Session, select, func, and_
from datetime import datetime, date
from models.task import Task, TaskStatus, TaskPriority
from models.todo import Todo


class DashboardService:
    """Service class for dashboard analytics"""

    @staticmethod
    def get_statistics(session: Session, user_id: int) -> dict:
        """Get comprehensive dashboard statistics"""
        # Total tasks
        total_tasks = session.exec(
            select(func.count(Task.id)).where(Task.user_id == user_id)
        ).one()

        # Completed tasks
        completed_tasks = session.exec(
            select(func.count(Task.id)).where(
                and_(Task.user_id == user_id, Task.status == TaskStatus.COMPLETED)
            )
        ).one()

        # Calculate completion percentage
        completion_percentage = (
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        )

        # Tasks by status
        status_counts = DashboardService.get_task_counts_by_status(session, user_id)

        # Tasks by priority
        priority_counts = DashboardService.get_task_counts_by_priority(session, user_id)

        # Overdue tasks
        today = date.today()
        overdue_tasks = session.exec(
            select(func.count(Task.id)).where(
                and_(
                    Task.user_id == user_id,
                    Task.due_date < datetime.combine(today, datetime.min.time()),
                    Task.status != TaskStatus.COMPLETED
                )
            )
        ).one()

        # Due today
        tomorrow = datetime.combine(date.today(), datetime.max.time())
        due_today = session.exec(
            select(func.count(Task.id)).where(
                and_(
                    Task.user_id == user_id,
                    Task.due_date <= tomorrow,
                    Task.due_date >= datetime.combine(today, datetime.min.time()),
                    Task.status != TaskStatus.COMPLETED
                )
            )
        ).one()

        # Total todos
        total_todos = session.exec(
            select(func.count(Todo.id)).where(Todo.user_id == user_id)
        ).one()

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_percentage": round(completion_percentage, 2),
            "status_breakdown": status_counts,
            "priority_breakdown": priority_counts,
            "overdue_tasks": overdue_tasks,
            "due_today": due_today,
            "total_todos": total_todos,
        }

    @staticmethod
    def get_recent_tasks(session: Session, user_id: int, limit: int = 5) -> list[dict]:
        """Get recently created tasks"""
        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
            .limit(limit)
        )
        tasks = session.exec(statement).all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
                "created_at": task.created_at,
            }
            for task in tasks
        ]

    @staticmethod
    def get_due_today_tasks(session: Session, user_id: int) -> list[dict]:
        """Get tasks due today"""
        today = date.today()
        statement = (
            select(Task)
            .where(
                and_(
                    Task.user_id == user_id,
                    Task.due_date >= datetime.combine(today, datetime.min.time()),
                    Task.due_date <= datetime.combine(today, datetime.max.time()),
                    Task.status != TaskStatus.COMPLETED
                )
            )
            .order_by(Task.due_date.asc())
        )
        tasks = session.exec(statement).all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
                "todo_id": task.todo_id,
            }
            for task in tasks
        ]

    @staticmethod
    def get_overdue_tasks(session: Session, user_id: int) -> list[dict]:
        """Get overdue tasks"""
        today = date.today()
        statement = (
            select(Task)
            .where(
                and_(
                    Task.user_id == user_id,
                    Task.due_date < datetime.combine(today, datetime.min.time()),
                    Task.status != TaskStatus.COMPLETED
                )
            )
            .order_by(Task.due_date.asc())
        )
        tasks = session.exec(statement).all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
                "todo_id": task.todo_id,
            }
            for task in tasks
        ]

    @staticmethod
    def get_task_counts_by_status(session: Session, user_id: int) -> dict[str, int]:
        """Get count of tasks by status"""
        statement = (
            select(Task.status, func.count(Task.id))
            .where(Task.user_id == user_id)
            .group_by(Task.status)
        )

        results = session.exec(statement).all()
        counts = {
            TaskStatus.TODO: 0,
            TaskStatus.IN_PROGRESS: 0,
            TaskStatus.COMPLETED: 0,
            TaskStatus.BLOCKED: 0,
        }

        for status, count in results:
            if status in counts:
                counts[status] = count

        return counts

    @staticmethod
    def get_task_counts_by_priority(session: Session, user_id: int) -> dict[str, int]:
        """Get count of tasks by priority"""
        statement = (
            select(Task.priority, func.count(Task.id))
            .where(Task.user_id == user_id)
            .group_by(Task.priority)
        )

        results = session.exec(statement).all()
        counts = {
            TaskPriority.LOW: 0,
            TaskPriority.MEDIUM: 0,
            TaskPriority.HIGH: 0,
            TaskPriority.URGENT: 0,
        }

        for priority, count in results:
            if priority in counts:
                counts[priority] = count

        return counts
