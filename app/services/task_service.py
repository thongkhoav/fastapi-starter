from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, aliased, joinedload
from app.core.environment import Environment
from app.models.room import Room
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.models.user_room import UserRoom
from app.schemas.task.create_task import CreateTaskRequest
from app.services import room_service

# Environment variables
read_env = Environment()


def create_task(
    db: Session,
    dto: CreateTaskRequest,
    current_user_id: int,
):
    # Check task due_date is before now
    if dto.due_date < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Due date must be in the future",
        )

    # Check room exist
    room = db.query(Room).filter(Room.id == dto.room_id).first()  # type: ignore
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    # Check current user is owner
    is_owner = room_service.is_room_owner(db, dto.room_id, current_user_id)
    if not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create task in this room",
        )

    # Check assigned user is in the room
    if dto.assigned_user_id:
        is_room_member = room_service.is_room_member_by_id(
            db, dto.room_id, dto.assigned_user_id
        )
        if not is_room_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Assigned user is not a member of the room",
            )

        # Check assigned user is not the owner
        if dto.assigned_user_id == current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Assigned user cannot be the room owner",
            )
    # Create task
    db_task = Task(
        title=dto.title,
        description=dto.description,
        due_date=dto.due_date,
        status=TaskStatus.TODO,
        room_id=room.id,
    )
    if dto.assigned_user_id:
        db_task.user_id = dto.assigned_user_id
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
