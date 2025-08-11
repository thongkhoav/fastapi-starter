from pydantic import BaseModel, EmailStr
from app.schemas.user.user_schema import TokenResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(TokenResponse):
    pass
