from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(
        ...,
        min_length=6,
        max_length=30,
        description="Password must be at least 6 characters long",
    )
