from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from app.schemas.user.user_schema import UserResponse
from app.schemas.user.signup_schema import SignupRequest
from app.schemas.user.login_schema import LoginResponse
from app.db.database import get_db_session
from app.services import user_service as user_service
from app.controllers import auth_controller
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=UserResponse)
def signup(user: SignupRequest, db: Session = Depends(get_db_session)):
    return auth_controller.signup_controller(db, user)


@router.post("/login", response_model=LoginResponse)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):
    return auth_controller.login_controller(response, db, form_data)
