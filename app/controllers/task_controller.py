from app.schemas.response.message_response import MessageResponse
from app.schemas.room.create_room_schema import CreateRoomRequest
from sqlalchemy.orm import Session
from app.schemas.task.create_task import CreateTaskRequest
from app.services import task_service


def create_task(db: Session, room_dto: CreateTaskRequest, current_user_id: int):
    task_service.create_task(db, room_dto, current_user_id)
    return MessageResponse(message="Task created successfully")
