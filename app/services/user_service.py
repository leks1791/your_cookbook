from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User

# Simple password hashing service (centralized for future refactoring)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])


def create_user(db: Session, username: str, email: str, password: str) -> User:
    hashed_password = hash_password(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
