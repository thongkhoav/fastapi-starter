from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.user.user_schema import BasicUser


class TaskItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: str
    user: Optional[BasicUser] = None
