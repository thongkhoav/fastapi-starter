from fastapi import HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user.login_schema import LoginRequest, LoginResponse
from app.schemas.user.signup_schema import SignupRequest
from app.utils import password
from sqlalchemy.orm import Session
from app.services import user_service
from app.schemas.user.user_schema import UserCreate, UserDBCreate
import uuid
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Token secret
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

# Cookie settings
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "False").lower() in ("true", "1", "yes")
COOKIE_HTTPONLY = os.getenv("COOKIE_HTTPONLY", "True").lower() in ("true", "1", "yes")
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "Lax")
COOKIE_ACCESS_TOKEN_NAME = os.getenv("COOKIE_ACCESS_TOKEN_NAME")
COOKIE_REFRESH_TOKEN_NAME = os.getenv("COOKIE_REFRESH_TOKEN_NAME")


def signup_controller(db: Session, user_data: SignupRequest):
    if user_service.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Hash the password before saving
    hashed_password = password.hash_password(user_data.password)
    user_create: UserDBCreate = UserDBCreate(
        name=user_data.name, email=user_data.email, password=hashed_password
    )
    return user_service.create_user(db, user_create)


def login_controller(
    response: Response, db: Session, form_data: OAuth2PasswordRequestForm
) -> LoginResponse:
    # form_data: username as email
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Access token creation
    access_token_payload = {
        "sub": user.email,
        "user_id": user.id,
        "fullName": user.fullName,
        "role": user.role,
    }
    access_token = user_service.create_access_token(access_token_payload)

    # Refresh token creation
    jti = str(uuid.uuid4())
    refresh_token_payload = {"sub": user.email, "user_id": user.id, "jti": jti}
    refresh_token = user_service.create_refresh_token(refresh_token_payload)

    # Set cookies
    response.set_cookie(
        key=COOKIE_ACCESS_TOKEN_NAME,
        value=access_token,
        httponly=COOKIE_HTTPONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # in seconds
    )

    response.set_cookie(
        key=COOKIE_REFRESH_TOKEN_NAME,
        value=refresh_token,
        httponly=COOKIE_HTTPONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,  # in seconds
    )

    return LoginResponse(access_token=access_token, refresh_token=refresh_token)
