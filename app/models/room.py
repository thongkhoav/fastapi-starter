from enum import Enum
from uuid import uuid4

from sqlalchemy import CheckConstraint
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship, String, Column

if TYPE_CHECKING:
    from .user_room import UserRoom
    from .task import Task


class Room(SQLModel, table=True):
    __tablename__ = "rooms"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(100), nullable=False))
    description: str = Field(sa_column=Column(String(500), nullable=False))
    invite_code: str = Field(sa_column=Column(String(255), nullable=False, unique=True))

    # Relationships
    user_rooms: list["UserRoom"] = Relationship(back_populates="room")
    tasks: list["Task"] = Relationship(back_populates="room")
