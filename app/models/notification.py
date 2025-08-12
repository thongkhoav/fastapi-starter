from enum import Enum
from uuid import uuid4

from sqlalchemy import CheckConstraint
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship, String, Column

if TYPE_CHECKING:
    from .user import User


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String(255), nullable=False))
    body: str = Field(sa_column=Column(String(1000), nullable=False))
    is_read: bool = Field(default=False, nullable=False)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    # Relationships
    user: Optional["User"] = Relationship(back_populates="notifications")
