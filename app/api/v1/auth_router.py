from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from app.middlewares.auth_middleware import get_current_user_from_token_or_cookie
from app.schemas.user.user_schema import UserResponse
from app.schemas.user.signup_schema import SignupRequest
from app.schemas.user.login_schema import LoginResponse
from app.db.database import get_db_session
from app.services import user_service as user_service
from app.controllers import auth_controller
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.path.auth_path import AuthPath

router = APIRouter(prefix="/auth")

# FORGOT PASSWORD
# RESET PASSWORD


# ME
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user_from_token_or_cookie)):
    return UserResponse.model_validate(current_user)


# SIGNUP
@router.post("/signup", response_model=UserResponse)
def signup(user: SignupRequest, db: Session = Depends(get_db_session)):
    return auth_controller.signup_controller(db, user)


# LOGIN
@router.post("/login", response_model=LoginResponse)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):
    return auth_controller.login_controller(response, db, form_data)


# REFRESH
