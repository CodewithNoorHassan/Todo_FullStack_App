from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from database.engine import engine
from models.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
from models.user import User
from auth.auth_handler import get_current_user
from services.todo_service import TodoService


router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("/", response_model=TodoListResponse)
def get_todos(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    with Session(engine) as session:
        todos, total = TodoService.get_todos(session, current_user.id, skip=skip, limit=limit)
        return {"todos": todos, "total": total, "skip": skip, "limit": limit}


@router.post("/", response_model=TodoResponse)
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        new_todo = TodoService.create_todo(session, current_user.id, todo)
        return new_todo


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        todo = TodoService.get_todo(session, current_user.id, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        updated = TodoService.update_todo(session, current_user.id, todo_id, todo_update)
        if not updated:
            raise HTTPException(status_code=404, detail="Todo not found")
        return updated


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        deleted = TodoService.delete_todo(session, current_user.id, todo_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Todo not found")

        return {"message": "Todo deleted successfully"}