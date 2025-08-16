from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class CreateRoomRequest(BaseModel):
    name: str
    description: str


class RoomOwner(BaseModel):
    id: int
    email: str
    full_name: str


class RoomInfoResponse(BaseModel):
    id: int
    name: str
    description: str
    owner: RoomOwner
    invite_path: str

    class Config:
        from_attributes = True
