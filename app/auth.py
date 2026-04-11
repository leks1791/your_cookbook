import logging
from datetime import UTC, datetime, timedelta

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from pydantic_settings import BaseSettings
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.user_service import create_user as create_user_service

logger = logging.getLogger(__name__)

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])


class Settings(BaseSettings):
    secret_key: str = "fallback-secret-key-do-not-use-in-production"
    algorithm: str = "HS256"
    access_token_expire_days: int = 7

    model_config = ConfigDict(env_file=".env")


settings = Settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


# Схемы
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Пароль должен быть не менее 6 символов")
        return v


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


# Роутеры регистрации и логина
@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Registration attempt for user: {user.username} ({user.email})")

        existing = (
            db.query(User)
            .filter((User.email == user.email) | (User.username == user.username))
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400, detail="Email or username already exists"
            )

        # Use service layer to create user (handles hashing and commit)
        new_user = create_user_service(db, user.username, user.email, user.password)  # type: ignore
        logger.info(f"User registered successfully: {new_user.id}")
        return new_user
    except IntegrityError:
        # Race condition protection: rollback and friendly message
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Email or username already exists"
        ) from None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        ) from e


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
    # bcrypt has a 72 byte limit, truncate if necessary
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


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    # Returns the current authenticated user's basic info
    return current_user
