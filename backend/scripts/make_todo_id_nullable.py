"""
Script to make task.todo_id column nullable (Postgres).
Run with the backend environment active:
    python scripts/make_todo_id_nullable.py
"""
from database.engine import engine
from app.config import settings

sql = None
if 'sqlite' in settings.database_url:
    print('SQLite detected. Manual migration required to alter column nullability.')
    exit(1)
else:
    # Postgres-compatible SQL
    sql = "ALTER TABLE task ALTER COLUMN todo_id DROP NOT NULL;"

with engine.connect() as conn:
    try:
        print('Executing:', sql)
        conn.execute(sql)
        conn.commit()
        print('✅ Column altered to nullable (todo_id)')
    except Exception as e:
        print('❌ Error running ALTER TABLE:', e)
        raise
