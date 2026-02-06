#!/usr/bin/env python3
"""
Database migration: Add status and priority enums to task table
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("NEON_DATABASE_URL") or os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL or NEON_DATABASE_URL not set")
    exit(1)

def migrate():
    """Apply database migration"""
    print(f"Connecting to database: {DATABASE_URL[:50]}...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Check if status column exists
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='task' AND column_name='status'
        """)
        
        if cur.fetchone():
            print("✓ status column already exists")
        else:
            print("Adding status column...")
            # Create enum type for TaskStatus
            cur.execute("DROP TYPE IF EXISTS taskstatus CASCADE;")
            cur.execute("""
                CREATE TYPE taskstatus AS ENUM ('TODO', 'IN_PROGRESS', 'COMPLETED', 'BLOCKED')
            """)
            # Add status column with default
            cur.execute("""
                ALTER TABLE task ADD COLUMN status taskstatus DEFAULT 'TODO'
            """)
            print("✓ Added status column")
        
        # Check if priority column exists
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='task' AND column_name='priority'
        """)
        
        if cur.fetchone():
            print("✓ priority column already exists")
        else:
            print("Adding priority column...")
            # Create enum type for TaskPriority
            cur.execute("DROP TYPE IF EXISTS taskpriority CASCADE;")
            cur.execute("""
                CREATE TYPE taskpriority AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'URGENT')
            """)
            # Add priority column with default
            cur.execute("""
                ALTER TABLE task ADD COLUMN priority taskpriority DEFAULT 'MEDIUM'
            """)
            print("✓ Added priority column")
        
        # Check if due_date column exists
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='task' AND column_name='due_date'
        """)
        
        if cur.fetchone():
            print("✓ due_date column already exists")
        else:
            print("Adding due_date column...")
            cur.execute("""
                ALTER TABLE task ADD COLUMN due_date TIMESTAMP NULL
            """)
            print("✓ Added due_date column")
        
        # Check if completed_at column exists
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='task' AND column_name='completed_at'
        """)
        
        if cur.fetchone():
            print("✓ completed_at column already exists")
        else:
            print("Adding completed_at column...")
            cur.execute("""
                ALTER TABLE task ADD COLUMN completed_at TIMESTAMP NULL
            """)
            print("✓ Added completed_at column")
        
        # Check if todo_id column exists
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='task' AND column_name='todo_id'
        """)
        
        if cur.fetchone():
            print("✓ todo_id column already exists")
        else:
            print("Adding todo_id column...")
            cur.execute("""
                ALTER TABLE task ADD COLUMN todo_id INTEGER REFERENCES todo(id)
            """)
            print("✓ Added todo_id column")
        
        # Check if completed column exists
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='task' AND column_name='completed'
        """)
        
        if cur.fetchone():
            print("✓ completed column already exists")
        else:
            print("Adding completed column...")
            cur.execute("""
                ALTER TABLE task ADD COLUMN completed BOOLEAN DEFAULT FALSE
            """)
            print("✓ Added completed column")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("\n✓ Migration completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        return 1

if __name__ == "__main__":
    exit(migrate())
