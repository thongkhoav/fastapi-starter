from pydantic import BaseModel, Field


class CreateRoomRequest(BaseModel):
    name: str
    description: str


class RoomOwner(BaseModel):
    id: int
    email: str
    full_name: str


class CreateRoomResponse(BaseModel):
    id: int
    name: str
    description: str
    owner: RoomOwner
    invite_code: str

    class Config:
        from_attributes = True
