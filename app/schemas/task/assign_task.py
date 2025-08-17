from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.models.task import TaskStatus


class AssignTaskRequest(BaseModel):
    user_id: int = Field(..., description="ID of the user to assign the task to")
