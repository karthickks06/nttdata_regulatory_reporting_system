#!/usr/bin/env python3
"""Create admin user (alternative to seed_data.py)"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.postgres import engine
from app.core.security import get_password_hash
from sqlalchemy import text
from datetime import datetime

def create_admin():
    """Create admin user if not exists"""
    with engine.connect() as conn:
        # Check if admin exists
        result = conn.execute(
            text("SELECT COUNT(*) FROM users WHERE username = :username"),
            {"username": "admin"}
        )
        if result.scalar() > 0:
            print("Admin user already exists")
            return

        # Create admin user
        hashed_password = get_password_hash("admin123")
        conn.execute(
            text("""
                INSERT INTO users (username, email, hashed_password, full_name,
                                 is_active, is_superuser, created_at, updated_at)
                VALUES (:username, :email, :password, :full_name,
                       :is_active, :is_superuser, :created_at, :updated_at)
            """),
            {
                "username": "admin",
                "email": "admin@nttdata.com",
                "password": hashed_password,
                "full_name": "System Administrator",
                "is_active": True,
                "is_superuser": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        )
        conn.commit()
        print("Admin user created (username: admin, password: admin123)")

if __name__ == "__main__":
    create_admin()
