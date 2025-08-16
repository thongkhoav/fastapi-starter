from pydantic import BaseModel, EmailStr, Field


class JoinRoomRequest(BaseModel):
    invite_path: str
