from typing import Optional
from pydantic import BaseModel


class RemoveRoomMemberRequest(BaseModel):
    user_id: int
    remove_all: Optional[bool] = False
