from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(
        ...,
        min_length=6,
        max_length=50,
        description="Password must be at least 6 characters long",
    )
