from fastapi import Depends, HTTPException, Cookie, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.environment import Environment
from sqlmodel import Session
from typing import Callable, Optional, List
from app.db.database import get_db_session
from jwt.exceptions import InvalidTokenError
from app.schemas.user.user_schema import CurrentUser
from app.services.user_service import get_user_by_email
import jwt
from fastapi.logger import logger
from app.schemas.user.token_schema import AccessTokenPayload

# Load environment variables
read_env = Environment()

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# API_VERSION = "/api/v1"

# PUBLIC_PATHS: List[str] = [
#     API_VERSION + AuthPath.BASE + AuthPath.LOGIN,
#     API_VERSION + AuthPath.BASE + AuthPath.SIGNUP,
#     "/docs",
#     "/redoc",
#     "/openapi.json",
# ]


# async def auth_middleware(request: Request, call_next, db: Session):
#     path = request.url.path

#     # Skip public paths
#     if path in PUBLIC_PATHS:
#         return await call_next(request)

#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     # Get token from header or cookie
#     access_token = None
#     auth_header = request.headers.get("Authorization")
#     if auth_header and auth_header.startswith("Bearer "):
#         access_token = auth_header.split(" ", 1)[1]

#     if not access_token:
#         access_token = request.cookies.get("access_token")

#     if not access_token:
#         raise credentials_exception

#     try:
#         # Decode the JWT token
#         payload = jwt.decode(
#             access_token,
#             read_env.ACCESS_TOKEN_SECRET_KEY,
#             algorithms=[read_env.ALGORITHM],
#         )

#         # Extract user email from token
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception

#         # Create token payload object
#         token_data = AccessTokenPayload(**payload)
#     except InvalidTokenError:
#         raise credentials_exception

#     # Get user from database
#     user = get_user_by_email(db, email)
#     logger.info(f"Authenticated user: {user.email if user else 'None'}")
#     if user is None:
#         raise credentials_exception

#     return await call_next(request)


async def get_current_user(
    access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)
) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid access token",
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

    return CurrentUser(**user.model_dump())


# Get user to use in request
async def get_current_active_user(
    current_user: CurrentUser = Depends(get_current_user),
):
    return current_user


# Get token from cookie
async def get_token_from_cookie(
    access_token: Optional[str] = Cookie(None, alias=read_env.COOKIE_ACCESS_TOKEN_NAME)
):
    if not access_token:
        return None
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
) -> CurrentUser:
    return await get_current_user(token, db)
