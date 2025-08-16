from pydantic import BaseModel, EmailStr, Field


class AddRoomMemberRequest(BaseModel):
    email: EmailStr
