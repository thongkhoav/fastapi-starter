from fastapi import HTTPException, status
from sqlalchemy.orm import Session, aliased, joinedload
from app.core.environment import Environment
from app.models.room import Room
from app.models.task import Task
from app.models.user import User
from app.models.user_room import UserRoom
from app.schemas.room.create_room_schema import (
    CreateRoomRequest,
    RoomInfoResponse,
    RoomOwner,
)
from app.schemas.room.remove_member import RemoveRoomMemberRequest
from app.schemas.room.room_schema import RoomUser
from app.schemas.room.update_room_schema import UpdateRoomRequest
from app.schemas.user.user_schema import BasicUser, CurrentUser
import uuid

# Environment variables
read_env = Environment()


# HANDLER


# Check start with INVITE_PREFIX
# Check if user exists, email is valid
# Check if user is already a member
def join_room_validator(
    db: Session,
    invite_path: str,
    current_user_id: int,
):
    if not invite_path.startswith(read_env.INVITE_PREFIX):
        raise HTTPException(
            status_code=400,
            detail="Invalid invite path",
        )
    uuid_invite_code = invite_path.split("/")[-1]
    print("uuid_invite_code", uuid_invite_code)
    # Check if room exists
    room = db.query(Room).filter(Room.invite_code == uuid_invite_code).first()  # type: ignore
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    # Check if user is already a member
    is_joined = db.query(UserRoom).filter(UserRoom.room_id == room.id, current_user_id == UserRoom.user_id).first()  # type: ignore
    if is_joined:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of the room",
        )


def join_room(
    db: Session,
    invite_path: str,
    current_user_id: int,
):
    uuid_invite_code = invite_path.split("/")[-1]
    room = db.query(Room).filter(Room.invite_code == uuid_invite_code).first()  # type: ignore
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )
    db_user_room = UserRoom(user_id=current_user_id, room_id=room.id, is_owner=False)
    db.add(db_user_room)
    db.commit()
    db.refresh(db_user_room)


# Check room is existingq
# Check if user exists, email is valid
# Check if user is already a member
# Check if current user is owner
def add_member_validator(db: Session, current_user_id: int, email: str, room_id: int):
    # Check if room exists
    room = db.query(Room).filter(Room.id == room_id).first()  # type: ignore
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    # Check if user exists, email is valid
    user = db.query(User).filter(User.email == email).first()  # type: ignore
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # Check if user is already a member
    is_added = db.query(UserRoom).filter(UserRoom.room_id == room_id, user.id == UserRoom.user_id).first()  # type: ignore
    if is_added:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of the room",
        )

    # Check if current user is owner
    is_owner = is_room_owner(db, room_id, current_user_id)
    if not is_owner:
        raise HTTPException(
            status_code=403,
            detail="Not a owner of the room",
        )


def add_member_by_email(db: Session, room_id: int, email: str):
    db_user = db.query(User).filter(User.email == email).first()  # type: ignore
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    db_user_room = UserRoom(user_id=db_user.id, room_id=room_id, is_owner=False)
    db.add(db_user_room)
    db.commit()
    db.refresh(db_user_room)


def is_room_owner(db: Session, room_id: int, user_id: int) -> bool:
    # print("check room owner", room_id, user_id)
    user_room = db.query(UserRoom).filter(UserRoom.room_id == room_id, UserRoom.user_id == user_id, UserRoom.is_owner == True).first()  # type: ignore
    # print("data", user_room)
    return user_room is not None


def create_room(
    db: Session, create_room: CreateRoomRequest, current_user: CurrentUser
) -> RoomInfoResponse:
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
    return RoomInfoResponse(
        id=db_room.id if db_room.id is not None else 0,
        name=db_room.name,
        description=db_room.description,
        owner=RoomOwner(
            id=current_user.id if current_user.id is not None else 0,
            email=current_user.email,
            full_name=current_user.full_name,
        ),
        invite_path=f"{read_env.INVITE_PREFIX}/{db_room.invite_code}",
    )


def update_room(
    db: Session, room_id: int, body: UpdateRoomRequest, current_user_id: int
):
    room = db.query(Room).filter(Room.id == room_id).first()  # type: ignore
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    # Check if current user is owner
    is_owner = is_room_owner(db, room_id, current_user_id)
    if not is_owner:
        raise HTTPException(
            status_code=403,
            detail="Not a owner of the room",
        )

    room.name = body.name
    room.description = body.description
    db.commit()
    db.refresh(room)


def is_room_member_by_email(db: Session, room_id: int, email: str) -> bool:
    return (
        db.query(UserRoom)
        .join(User, UserRoom.user_id == User.id)  # type: ignore
        .filter(UserRoom.room_id == room_id, User.email == email)  # type: ignore
        .first()
        is not None
    )


def is_room_member_by_id(db: Session, room_id: int, user_id: int) -> bool:
    print("check room member", room_id, user_id)
    return (
        db.query(UserRoom)
        .filter(UserRoom.room_id == room_id, UserRoom.user_id == user_id)  # type: ignore
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


def get_room_by_id(db: Session, room_id: int):
    result = db.query(UserRoom).options(joinedload(UserRoom.user), joinedload(UserRoom.room)).filter(UserRoom.room_id == room_id, UserRoom.is_owner == True).first()  # type: ignore
    if result is None or result.room is None or result.user is None:
        return None
    print("owner user", result.user)
    return RoomInfoResponse(
        id=result.room_id if result.room_id is not None else 0,
        name=result.room.name,
        description=result.room.description,
        owner=RoomOwner(
            id=result.user.id if result.user.id is not None else 0,
            email=result.user.email,
            full_name=result.user.full_name,
        ),
        invite_path=f"{read_env.INVITE_PREFIX}/{result.room.invite_code}",
    )


def get_room_users(db: Session, room_id: int, include_owner: bool = False):
    query = db.query(User, UserRoom.is_owner).join(UserRoom).filter(UserRoom.room_id == room_id)  # type: ignore
    if not include_owner:
        query = query.filter(UserRoom.is_owner == False)  # type: ignore
    results = query.all()  # type: ignore
    return [RoomUser(user=user, is_owner=is_owner) for user, is_owner in results]


def delete_room(db: Session, room_id: int, current_user_id: int):
    # Check room owner
    is_owner = is_room_owner(db, room_id, current_user_id)
    if not is_owner:
        raise HTTPException(status_code=403, detail="Not the room owner")
    # Check if room exists
    room = db.query(Room).filter(Room.id == room_id).first()  # type: ignore
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Remove room
    # remove user_room, then remove tasks
    db.query(UserRoom).filter(UserRoom.room_id == room_id).delete()  # type: ignore
    db.query(Task).filter(Task.room_id == room_id).delete()  # type: ignore
    db.delete(room)
    db.commit()


def remove_member(
    db: Session, room_id: int, body: RemoveRoomMemberRequest, current_user_id: int
):
    # Check if room exists
    room = db.query(Room).filter(Room.id == room_id).first()  # type: ignore
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Check room owner
    is_owner = is_room_owner(db, room_id, current_user_id)
    if not is_owner:
        raise HTTPException(status_code=403, detail="Not the room owner")

    if not body.remove_all and body.user_id is not None:
        # Check if user is in room
        is_member = is_room_member_by_id(db, room_id, body.user_id)
        if not is_member:
            raise HTTPException(status_code=404, detail="User not found in room")

        if is_room_owner(db, room_id, body.user_id):
            raise HTTPException(status_code=403, detail="Cannot remove room owner")

        # Remove member with assigned tasks also
        db.query(Task).filter(Task.room_id == room_id, Task.user_id == body.user_id).update({Task.user_id: None})  # type: ignore
        db.query(UserRoom).filter(
            UserRoom.room_id == room_id,  # type: ignore
            UserRoom.user_id == body.user_id,  # type: ignore
            UserRoom.is_owner == False,  # type: ignore
        ).delete()
    else:
        # Remove all members except owners and delete associated tasks
        db.query(Task).filter(Task.room_id == room_id, Task.user_id != current_user_id).update({Task.user_id: None})  # type: ignore
        db.query(UserRoom).filter(UserRoom.room_id == room_id, UserRoom.is_owner == False).delete()  # type: ignore
    db.commit()


def leave_room(db: Session, room_id: int, current_user_id: int):
    # Check if room exists
    room = db.query(Room).filter(Room.id == room_id).first()  # type: ignore
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )
    print("room user ", room_id, current_user_id)
    # Check room owner
    is_owner = is_room_owner(db, room_id, current_user_id)
    if is_owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room owner cannot leave the room",
        )

    db.query(Task).filter(Task.room_id == room_id, Task.user_id == current_user_id).update({Task.user_id: None})  # type: ignore
    db.query(UserRoom).filter(
        UserRoom.room_id == room_id,  # type: ignore
        UserRoom.user_id == current_user_id,  # type: ignore
        UserRoom.is_owner == False,  # type: ignore
    ).delete()
    db.commit()
