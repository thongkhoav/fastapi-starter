from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CreateTaskRequest(BaseModel):
    title: str = Field(..., max_length=255, description="Title of the task")
    description: Optional[str] = Field(
        None, max_length=1000, description="Description of the task"
    )
    due_date: datetime = Field(..., description="Due date of the task")
    room_id: int = Field(..., description="ID of the room to which the task belongs")
    assigned_user_id: Optional[int] = Field(
        None, description="ID of the user to whom the task is assigned"
    )
