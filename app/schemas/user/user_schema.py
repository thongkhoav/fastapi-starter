from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    full_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserDBCreate(UserBase):
    hashed_password: str


class CurrentUser(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True


class BasicUser(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
