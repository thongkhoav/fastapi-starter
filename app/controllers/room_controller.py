from app.schemas.room.create_room_schema import CreateRoomRequest
from sqlalchemy.orm import Session
from app.services import room_service
from app.schemas.user.user_schema import CurrentUser


def create_room(db: Session, room_dto: CreateRoomRequest, current_user: CurrentUser):
    return room_service.create_room(db, room_dto, current_user)


def get_user_rooms(db: Session, user_id: int):
    return room_service.get_user_rooms(db, user_id)
