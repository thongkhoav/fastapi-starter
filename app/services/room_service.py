from sqlalchemy.orm import Session, aliased
from app.core.environment import Environment
from app.models.room import Room
from app.models.user import User
from app.models.user_room import UserRoom
from app.schemas.room.create_room_schema import (
    CreateRoomRequest,
    CreateRoomResponse,
    RoomOwner,
)
from app.schemas.user.user_schema import BasicUser, CurrentUser
import uuid

# Environment variables
read_env = Environment()


# Handler
def create_room(
    db: Session, create_room: CreateRoomRequest, current_user: CurrentUser
) -> CreateRoomResponse:
    # Create room
    invite_code = str(uuid.uuid4())
    db_room = Room(
        name=create_room.name,
        description=create_room.description,
        invite_code=invite_code,
    )
    db.add(db_room)
    db.flush()

    # Create user_room with is_owner: True
    db_user_room = UserRoom(user_id=current_user.id, room_id=db_room.id, is_owner=True)
    db.add(db_user_room)
    db.commit()
    db.refresh(db_room)
    return CreateRoomResponse(
        id=db_room.id if db_room.id is not None else 0,
        name=db_room.name,
        description=db_room.description,
        owner=RoomOwner(
            id=current_user.id if current_user.id is not None else 0,
            email=current_user.email,
            full_name=current_user.full_name,
        ),
        invite_code=f"{read_env.INVITE_PREFIX}/{db_room.invite_code}",
    )


def is_room_member_by_email(db: Session, room_id: int, email: str) -> bool:
    return (
        db.query(UserRoom)
        .join(User, UserRoom.user_id == User.id)  # type: ignore
        .filter(UserRoom.room_id == room_id, User.email == email)  # type: ignore
        .first()
        is not None
    )


def get_user_rooms(db: Session, user_id: int):
    owner_ur = aliased(UserRoom)
    owner_user = aliased(User)

    # Example
    # SELECT r.*, ou.*
    # FROM room r
    # JOIN user_room ur ON r.id = ur.room_id
    # AND ur.user_id = :current_user_id
    # JOIN user_room owner_ur ON owner_ur.room_id = r.id
    # AND owner_ur.owner = TRUE
    # JOIN "user" ou ON ou.id = owner_ur.user_id;
    results = (
        db.query(Room, owner_user)
        .join(UserRoom, Room.id == UserRoom.room_id)  # type: ignore
        .filter(UserRoom.user_id == user_id)  # type: ignore
        .join(owner_ur, owner_ur.room_id == Room.id)  # type: ignore
        .filter(owner_ur.is_owner == True)  # type: ignore
        .join(owner_user, owner_user.id == owner_ur.user_id)  # type: ignore
        .all()
    )

    return [
        {"room": room, "owner": BasicUser.model_validate(owner)}
        for room, owner in results
    ]
