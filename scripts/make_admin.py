#!/usr/bin/env python
"""
Скрипт для назначения роли админа пользователю.
Использование: python scripts/make_admin.py <username>
"""

import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.user import User


def make_admin(username: str) -> None:
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"Пользователь '{username}' не найден")
            sys.exit(1)
        
        user.role = "admin"
        db.commit()
        print(f"✓ Пользователь '{username}' теперь администратор")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python scripts/make_admin.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    make_admin(username)
