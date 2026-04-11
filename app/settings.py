from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database URL (default to sqlite in project root)
    DATABASE_URL: str = "sqlite:///./recipes.db"

    class Config:
        env_file = ".env"


settings = Settings()
