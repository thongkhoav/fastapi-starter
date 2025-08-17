from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UpdateRoomRequest(BaseModel):
    name: str
    description: str
