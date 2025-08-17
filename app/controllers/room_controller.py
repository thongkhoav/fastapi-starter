from fastapi import HTTPException
from app.schemas.response.message_response import MessageResponse
from app.schemas.room.create_room_schema import CreateRoomRequest
from sqlalchemy.orm import Session
from app.schemas.room.remove_member import RemoveRoomMemberRequest
from app.schemas.room.update_room_schema import UpdateRoomRequest
from app.services import room_service
from app.schemas.user.user_schema import CurrentUser


def create_room(db: Session, room_dto: CreateRoomRequest, current_user: CurrentUser):
    return room_service.create_room(db, room_dto, current_user)


def get_user_rooms(db: Session, user_id: int):
    return room_service.get_user_rooms(db, user_id)


def get_room(db: Session, room_id: int, user_id: int):
    is_room_member = room_service.is_room_member_by_id(db, room_id, user_id)
    if not is_room_member:
        raise HTTPException(
            status_code=403,
            detail="Not a member of the room",
        )
    return room_service.get_room_by_id(db, room_id)


def add_member_by_email(db: Session, room_id: int, email: str, current_user_id: int):
    room_service.add_member_validator(db, current_user_id, email, room_id)
    room_service.add_member_by_email(db, room_id, email)
    return MessageResponse(message="User added to room successfully")


def join_room(db: Session, invite_path: str, user_id: int):
    room_service.join_room_validator(db, invite_path, user_id)
    room_service.join_room(db, invite_path, user_id)
    return MessageResponse(message="User joined the room successfully")


def get_room_users(db: Session, room_id: int, include_owner: bool = False):
    return room_service.get_room_users(db, room_id, include_owner)


def delete_room(db: Session, room_id: int, current_user_id: int):
    room_service.delete_room(db, room_id, current_user_id)
    return MessageResponse(message="Room deleted successfully")


def remove_member(
    db: Session, room_id: int, body: RemoveRoomMemberRequest, current_user_id: int
):
    room_service.remove_member(db, room_id, body, current_user_id)
    return MessageResponse(message="User removed from room successfully")


def leave_room(db: Session, room_id: int, current_user_id: int):
    room_service.leave_room(db, room_id, current_user_id)
    return MessageResponse(message="User left the room successfully")


def update_room(
    db: Session, room_id: int, body: UpdateRoomRequest, current_user_id: int
):
    room_service.update_room(db, room_id, body, current_user_id)
    return MessageResponse(message="Room updated successfully")
