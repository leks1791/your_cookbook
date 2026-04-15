from app.database import SessionLocal
from app.models.user import User
from app.auth import hash_password

db = SessionLocal()
try:
    existing = db.query(User).filter(User.username == 'admin').first()
    if existing:
        print('Пользователь admin уже существует')
    else:
        user = User(
            username='admin',
            email='admin@recipebook.local',
            hashed_password=hash_password('admin123'),
            role='admin'
        )
        db.add(user)
        db.commit()
        print('Пользователь admin создан с ролью администратора')
        print('Логин: admin')
        print('Пароль: admin123')
except Exception as e:
    db.rollback()
    print(f'Ошибка: {e}')
finally:
    db.close()
