from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)


class Todo(TodoBase, table=True):
    """Todo model representing todo lists"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TodoCreate(TodoBase):
    """Schema for creating a new todo"""
    pass


class TodoUpdate(SQLModel):
    """Schema for updating a todo"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)


class TodoResponse(TodoBase):
    """Schema for todo response"""
    id: int
    user_id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoListResponse(SQLModel):
    """Schema for todo list response with pagination"""
    todos: list["TodoResponse"]
    total: int
    skip: int
    limit: int