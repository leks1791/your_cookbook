from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# DATABASE_URL is now sourced from settings for easier configuration/testing
DATABASE_URL = None
try:
    from app.settings import settings as app_settings  # type: ignore
    DATABASE_URL = app_settings.DATABASE_URL
except Exception:
    DATABASE_URL = "sqlite:///./recipes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
