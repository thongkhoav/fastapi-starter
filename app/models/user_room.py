from enum import Enum
from uuid import uuid4
from sqlalchemy import (
    Column,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    CheckConstraint,
)
from app.db.base import Base


class User_Room(Base):
    __tablename__ = "user_rooms"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True
    )
