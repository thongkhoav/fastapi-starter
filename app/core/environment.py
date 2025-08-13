from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Environment(BaseSettings):
    # Database
    PG_USER: str = "SYS"
    PG_PASSWORD: str = "12345"
    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_DATABASE: str = "fast_task"

    # Backend
    ACCESS_TOKEN_SECRET_KEY: str = "your_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # in minutes
    ALGORITHM: str = "HS256"
    REFRESH_TOKEN_SECRET_KEY: str = "your_refresh_secret_key"
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 600  # in minutes
    JWT_RESET_SECRET: str = (
        "your_jwt_reset_secret"  # Secret for JWT reset password token
    )
    JWT_RESET_DURATION: str = "15m"  # Duration for reset password token

    COOKIE_ACCESS_TOKEN_NAME: str = "access_token"
    COOKIE_REFRESH_TOKEN_NAME: str = "refresh_token"
    COOKIE_SECURE: bool = False  # Set to True in production when using HTTPS
    COOKIE_HTTPONLY: bool = (
        True  # Set to True to prevent client-side access to the cookie
    )
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = (
        "none"  # Set SameSite attribute for cookies
    )
    ENVIRONMENT: str = "development"
    SEED_ON_STARTUP: bool = False
    OVERWRITE_DB: bool = False
    INVITE_PREFIX: str = "task_app/invite"

    FRONTEND_URL: str = "http://localhost:3000"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
