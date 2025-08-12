from enum import Enum
from uuid import uuid4

from sqlalchemy import CheckConstraint
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship, String, Column

if TYPE_CHECKING:
    from .user import User
    from .room import Room


class UserRoom(SQLModel, table=True):
    __tablename__ = "user_rooms"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    room_id: Optional[int] = Field(default=None, foreign_key="rooms.id")
    is_owner: bool = Field(default=False, nullable=False)

    # Relationships
    user: Optional["User"] = Relationship(
        back_populates="user_rooms"
    )  # back_populates user_rooms because user model has user_rooms relationship
    room: Optional["Room"] = Relationship(
        back_populates="user_rooms"
    )  # back_populates user_rooms because room model has user_rooms relationship
