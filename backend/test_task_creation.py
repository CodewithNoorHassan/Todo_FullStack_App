#!/usr/bin/env python3
"""
Test script to debug task creation issues
"""
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def test_task_creation():
    """Test creating a task"""
    from sqlmodel import Session
    from database.engine import engine
    from models.user import User
    from models.todo import Todo
    from models.task import Task, TaskCreate, TaskStatus, TaskPriority
    
    print("🧪 Testing task creation...")
    
    try:
        with Session(engine) as session:
            # Check if we have a user
            user = session.query(User).first()
            if not user:
                print("❌ No users found in database")
                return False
            
            print(f"✅ Found user: {user.email}")
            
            # Check if we have a todo
            todo = session.query(Todo).filter(Todo.user_id == user.id).first()
            if not todo:
                print("❌ No todos found for user")
                # Create one
                print("📝 Creating a test todo...")
                todo = Todo(
                    user_id=user.id,
                    title="Test Project",
                    description="Test project for task creation"
                )
                session.add(todo)
                session.commit()
                session.refresh(todo)
                print(f"✅ Created todo: {todo.id}")
            
            print(f"✅ Found todo: {todo.id} - {todo.title}")
            
            # Try to create a task
            print("📝 Creating a task...")
            task_create = TaskCreate(
                title="Test Task",
                description="Test task description",
                todo_id=todo.id,
                status=TaskStatus.TODO,
                priority=TaskPriority.MEDIUM
            )
            
            task = Task(
                user_id=user.id,
                todo_id=task_create.todo_id,
                title=task_create.title,
                description=task_create.description,
                status=task_create.status,
                priority=task_create.priority,
                due_date=task_create.due_date,
            )
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            print(f"✅ Task created successfully: {task.id} - {task.title}")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_task_creation()
    sys.exit(0 if success else 1)
