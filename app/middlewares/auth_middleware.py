from fastapi import Depends, HTTPException, Cookie, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.environment import Environment
from sqlmodel import Session
from typing import Optional
from app.models.user import User
from app.db.database import get_db_session
from jwt.exceptions import InvalidTokenError
from app.services.user_service import get_user_by_email
import jwt

from app.schemas.user.token_schema import AccessTokenPayload

# Load environment variables
read_env = Environment()

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(
            access_token,
            read_env.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[read_env.ALGORITHM],
        )

        # Extract user email from token
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        # Create token payload object
        token_data = AccessTokenPayload(**payload)
    except InvalidTokenError:
        raise credentials_exception

    # Get user from database
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


# Get user to use in request
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


# Get token from cookie
async def get_token_from_cookie(
    access_token: Optional[str] = Cookie(None, alias=read_env.COOKIE_ACCESS_TOKEN_NAME)
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not found in cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return access_token


# Get token from header or cookie
async def get_token(
    token_from_cookie: Optional[str] = Depends(get_token_from_cookie),
    token_from_header: Optional[str] = Depends(oauth2_scheme),
):
    if token_from_header:
        return token_from_header
    if token_from_cookie:
        return token_from_cookie

    # If no token is found, raise an exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No valid token found",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user_from_token_or_cookie(
    token: str = Depends(get_token), db: Session = Depends(get_db_session)
):
    return await get_current_user(token, db)
