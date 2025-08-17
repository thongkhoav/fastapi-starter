from typing import Optional
from app.schemas.response.message_response import MessageResponse
from app.schemas.room.create_room_schema import CreateRoomRequest
from sqlalchemy.orm import Session
from app.schemas.task.create_task import CreateTaskRequest
from app.services import task_service


def create_task(db: Session, room_dto: CreateTaskRequest, current_user_id: int):
    task_service.create_task(db, room_dto, current_user_id)
    return MessageResponse(message="Task created successfully")


def get_tasks(db: Session, room_id: int, user_id: Optional[int] = None):
    return task_service.get_tasks(db, room_id, user_id)
