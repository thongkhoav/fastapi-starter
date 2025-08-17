from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.models.task import TaskStatus


class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatus = Field(..., description="New status of the task")
