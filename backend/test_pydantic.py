#!/usr/bin/env python3
"""
Test Pydantic validation for TaskCreate
"""
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def test_pydantic():
    """Test Pydantic validation"""
    from models.task import TaskCreate, TaskStatus, TaskPriority
    import json
    
    print("🧪 Testing Pydantic TaskCreate validation...")
    
    try:
        # Test 1: Basic creation with all fields
        payload1 = {
            "title": "Test Task",
            "description": "Test description",
            "todo_id": 1,
            "status": "TODO",
            "priority": "MEDIUM"
        }
        
        print(f"📝 Payload 1: {json.dumps(payload1, indent=2)}")
        task1 = TaskCreate(**payload1)
        print(f"✅ Validation passed: {task1}")
        
        # Test 2: Minimal creation
        payload2 = {
            "title": "Test Task 2",
            "todo_id": 2
        }
        
        print(f"\n📝 Payload 2: {json.dumps(payload2, indent=2)}")
        task2 = TaskCreate(**payload2)
        print(f"✅ Validation passed: {task2}")
        
        # Test 3: With due_date
        payload3 = {
            "title": "Test Task 3",
            "todo_id": 3,
            "due_date": "2026-02-15T10:30:00"
        }
        
        print(f"\n📝 Payload 3: {json.dumps(payload3, indent=2)}")
        task3 = TaskCreate(**payload3)
        print(f"✅ Validation passed: {task3}")
        
        print("\n✅ All Pydantic validations passed!")
        return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pydantic()
    sys.exit(0 if success else 1)
