from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from app.middlewares.auth_middleware import get_current_user_from_token_or_cookie
from app.models.user import User
from app.schemas.room.add_room_member import AddRoomMemberRequest
from app.schemas.room.create_room_schema import CreateRoomRequest
from app.schemas.room.join_room import JoinRoomRequest
from app.schemas.room.remove_member import RemoveRoomMemberRequest
from app.schemas.user.user_schema import CurrentUser, UserResponse
from app.schemas.user.signup_schema import SignupRequest
from app.schemas.user.login_schema import LoginResponse
from app.db.database import get_db_session
from app.services import user_service as user_service
from app.controllers import room_controller
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/rooms")


# Post, :roomId/add-member
@router.post("/{room_id}/add_member")
def add_member_by_mail(
    body: AddRoomMemberRequest,
    room_id: int,
    db: Session = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return room_controller.add_member_by_email(db, room_id, body.email, current_user.id)


# Post, join-by-invite
@router.post("/join-by-invite")
def join_room_by_invite(
    body: JoinRoomRequest,
    db: Session = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return room_controller.join_room(db, body.invite_path, current_user.id)


# Post, /
@router.post("/")
def create_room(
    room_dto: CreateRoomRequest,
    db: Session = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return room_controller.create_room(db, room_dto, current_user)


# Get users of room, /:roomId/users
@router.get("/{room_id}/users")
def get_room_users(
    room_id: int,
    include_owner: bool = True,
    db: Session = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return room_controller.get_room_users(db, room_id, include_owner)


# Delete room, :roomId
@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return room_controller.delete_room(db, room_id, current_user.id)


#  Delete('/:roomId/remove-member')
@router.delete("/{room_id}/remove-member")
def remove_member(
    room_id: int,
    body: RemoveRoomMemberRequest,
    db: Session = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return room_controller.remove_member(db, room_id, body, current_user.id)


# @Put('/:roomId/leave')

# @Put('/:roomId'), update room


# Get, /
@router.get("/")
def get_user_rooms(
    db: Session = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return room_controller.get_user_rooms(db, current_user.id)


# Get, /room_id
@router.get("/{room_id}")
def get_room(
    room_id: int,
    db: Session = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user_from_token_or_cookie),
):
    return room_controller.get_room(db, room_id, current_user.id)
