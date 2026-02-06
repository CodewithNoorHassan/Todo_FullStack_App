#!/usr/bin/env python3
import os
import sys
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from auth.config import auth_settings
from jose import jwt
import requests
from sqlmodel import Session
from database.engine import engine
from models.user import User
from models.todo import Todo

with Session(engine) as session:
    user = session.exec("select * from user limit 1").first() if False else session.query(User).first()
    if not user:
        print('No user found')
        sys.exit(1)
    token = jwt.encode({"sub": user.email, "email": user.email}, auth_settings.secret_key, algorithm=auth_settings.algorithm)
    print('Using token:', token[:40]+"...")
    todo = session.query(Todo).filter(Todo.user_id == user.id).first()
    if not todo:
        print('No todo for user')
        sys.exit(1)

payload = {
    "title": "API Test Task",
    "description": "Created by api_request_test",
    "todo_id": todo.id,
    "priority": "MEDIUM",
    "status": "TODO"
}

resp = requests.post('http://localhost:8000/api/tasks', json=payload, headers={"Authorization": f"Bearer {token}"})
print('Status:', resp.status_code)
try:
    print('Body:', resp.json())
except Exception as e:
    print('Body non-json:', resp.text)
