"""File with settings and configs for the project"""
import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Settings for FastAPI application"""

    # FastAPI
    APP_PORT = os.environ.get("APP_PORT", default=8002)

    # token
    SECRET_KEY: str = os.environ.get("SECRET_KEY", default="secret_key")
    ALGORITHM: str = os.environ.get("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get(
        "ACCESS_TOKEN_EXPIRE_MINUTES", default=30
    )

    # GMAIL
    SMTP_USER = os.environ.get("SMTP_USER", default="")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", default="")
    SMTP_HOST = os.environ.get("SMTP_HOST", default="")
    SMTP_PORT = os.environ.get("SMTP_PORT", default=465)

    # PostgreSQL
    PG_USER = os.environ.get("PG_DB_2402_USER", default="postgres")
    PG_PWS = os.environ.get("PG_DB_2402_PASSWORD", default="postgres")
    PG_HOST = os.environ.get("PG_DB_2402_HOST", default="db_pg_2402")  # localhost
    PG_PORT = os.environ.get("PG_DB_2402_PORT", default=5432)
    PG_DB = os.environ.get("PG_DB_2402_DB", default="postgres")
    # connect string for the real database
    REAL_DATABASE_URL = (
        f"postgresql+asyncpg://{PG_USER}:{PG_PWS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    )


settings = Settings()
