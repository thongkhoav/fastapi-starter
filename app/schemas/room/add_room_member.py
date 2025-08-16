from pydantic import BaseModel, Field


class AddRoomMemberRequest(BaseModel):
    email: str
