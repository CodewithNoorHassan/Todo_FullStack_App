from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Any
from database.session import get_session
from auth.jwt_handler import get_current_user
from models.user import User
from services.dashboard_service import DashboardService


router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/", response_model=Any)
def get_dashboard(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Return dashboard statistics and recent tasks for the authenticated user."""
    stats = DashboardService.get_statistics(session, current_user.id)
    recent = DashboardService.get_recent_tasks(session, current_user.id, limit=5)
    due_today = DashboardService.get_due_today_tasks(session, current_user.id)
    overdue = DashboardService.get_overdue_tasks(session, current_user.id)

    return {
        "stats": stats,
        "recent_tasks": recent,
        "due_today": due_today,
        "overdue": overdue,
    }
