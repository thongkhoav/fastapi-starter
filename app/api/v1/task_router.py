from typing import Optional
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from app.middlewares.auth_middleware import get_current_user_from_token_or_cookie
from app.models.user import User
from app.schemas.room.add_room_member import AddRoomMemberRequest
from app.schemas.room.create_room_schema import CreateRoomRequest
from app.schemas.room.join_room import JoinRoomRequest
from app.schemas.room.remove_member import RemoveRoomMemberRequest
from app.schemas.room.update_room_schema import UpdateRoomRequest
from app.schemas.task.create_task import CreateTaskRequest
from app.schemas.task.update_task import UpdateTaskrequest
from app.schemas.user.user_schema import CurrentUser, UserResponse
from app.db.database import get_db_session
from app.services import user_service as user_service
from app.controllers import task_controller

router = APIRouter(prefix="/tasks")


# Post, /
@router.post("/")
def create_task(
    body: CreateTaskRequest,
    db: Session = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return task_controller.create_task(db, body, current_user.id)


# Get tasks of user
@router.get("/room/{room_id}")
def get_tasks(
    room_id: int,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db_session),
    _: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return task_controller.get_tasks(db, room_id, user_id)


# Update task info
@router.patch("/{task_id}/update-task-info")
def update_task_info(
    task_id: int,
    body: UpdateTaskrequest,
    db: Session = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return task_controller.update_task(db, task_id, body, current_user.id)


# Assign task
