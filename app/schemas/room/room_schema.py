from pydantic import BaseModel, Field

from app.schemas.user.user_schema import BasicUser


class RoomUser(BaseModel):
    user: BasicUser
    is_owner: bool
