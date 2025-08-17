from typing import Optional
from app.schemas.response.message_response import MessageResponse
from app.schemas.room.create_room_schema import CreateRoomRequest
from sqlalchemy.orm import Session
from app.schemas.task.assign_task import AssignTaskRequest
from app.schemas.task.create_task import CreateTaskRequest
from app.schemas.task.update_status import UpdateTaskStatusRequest
from app.schemas.task.update_task import UpdateTaskrequest
from app.services import task_service


def create_task(db: Session, dto: CreateTaskRequest, current_user_id: int):
    task_service.create_task(db, dto, current_user_id)
    return MessageResponse(message="Task created successfully")


def update_task(
    db: Session, task_id: int, dto: UpdateTaskrequest, current_user_id: int
):
    task_service.update_task(db, task_id, dto, current_user_id)
    return MessageResponse(message="Task updated successfully")


def update_task_status(
    db: Session, task_id: int, dto: UpdateTaskStatusRequest, current_user_id: int
):
    task_service.update_task_status(db, task_id, dto, current_user_id)
    return MessageResponse(message="Task status updated successfully")


def assign_task(
    db: Session, task_id: int, dto: AssignTaskRequest, current_user_id: int
):
    task_service.assign_task(db, task_id, dto, current_user_id)
    return MessageResponse(message="Task assigned successfully")


def get_tasks(db: Session, room_id: int, user_id: Optional[int] = None):
    return task_service.get_tasks(db, room_id, user_id)
