import logging
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.settings import settings
from app.services.user_service import create_user as create_user_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value


class UserLogin(BaseModel):
    email: str | None = None
    email_or_username: str | None = None
    password: str

    def get_login_field(self) -> str:
        return self.email_or_username or self.email or ""


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: str


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Registration attempt for user=%s email=%s", user.username, user.email)

        existing = (
            db.query(User)
            .filter((User.email == user.email) | (User.username == user.username))
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400, detail="Email or username already exists"
            )

        new_user = create_user_service(db, user.username, user.email, user.password)
        logger.info("User registered successfully: id=%s", new_user.id)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Email or username already exists"
        ) from None
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Registration error", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    login_field = user.get_login_field()

    if not login_field:
        raise HTTPException(status_code=422, detail="Email or username is required")

    db_user = (
        db.query(User)
        .filter((User.email == login_field) | (User.username == login_field))
        .first()
    )

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": db_user.id})
    return {"access_token": token}


def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=settings.access_token_expire_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(
    token: str = Depends(security), db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(
            token.credentials, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: int = payload.get("user_id")  # type: ignore
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token") from None

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
