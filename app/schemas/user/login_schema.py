from pydantic import BaseModel, EmailStr, Field
from app.schemas.user.user_schema import TokenResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=6,
        max_length=50,
        description="Password must be at least 6 characters long",
    )


class LoginResponse(TokenResponse):
    pass
