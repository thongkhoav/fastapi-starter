from enum import Enum
from uuid import uuid4

from sqlalchemy import CheckConstraint
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship, String, Column

if TYPE_CHECKING:
    from .user import User


class LoginSession(SQLModel, table=True):
    __tablename__ = "login_sessions"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    fcm_token: Optional[str] = Field(max_length=255, default=None, nullable=True)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="login_sessions")
