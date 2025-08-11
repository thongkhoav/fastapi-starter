from pydantic_settings import BaseSettings


class Environment(BaseSettings):
    # Database
    ORACLE_USER: str = "SYS"
    ORACLE_PASSWORD: str = "12345"
    ORACLE_HOST: str = "localhost"
    ORACLE_PORT: int = 1521
    ORACLE_SERVICE_NAME: str = "ORCLPDB"
    ORACLE_ROLE: str = "SYSDBA"

    # Backend
    ACCESS_TOKEN_SECRET_KEY: str = "your_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # in minutes
    ALGORITHM: str = "HS256"
    REFRESH_TOKEN_SECRET_KEY: str = "your_refresh_secret_key"
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 600  # in minutes

    COOKIE_ACCESS_TOKEN_NAME: str = "access_token"
    COOKIE_REFRESH_TOKEN_NAME: str = "refresh_token"
    COOKIE_SECURE: bool = False  # Set to True in production when using HTTPS
    COOKIE_HTTPONLY: bool = (
        True  # Set to True to prevent client-side access to the cookie
    )
    COOKIE_SAMESITE: str = "Lax"  # Set SameSite attribute for cookies
    ENVIRONMENT: str = "development"
    SEED_ON_STARTUP: bool = False
    OVERWRITE_DB: bool = False

    FRONTEND_URL: str = "http://localhost:3000"
