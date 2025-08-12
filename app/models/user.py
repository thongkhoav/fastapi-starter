from enum import Enum
from uuid import uuid4

from sqlalchemy import CheckConstraint
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship, String, Column

if TYPE_CHECKING:
    from .user_room import UserRoom
    from .task import Task
    from .login_session import LoginSession
    from .notification import Notification


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=100, nullable=False)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    role: UserRole = Field(
        default=UserRole.USER.value, sa_column=Column(String(20), nullable=False)
    )

    # Relationships
    user_rooms: list["UserRoom"] = Relationship(back_populates="user")
    tasks: list["Task"] = Relationship(back_populates="user")
    login_sessions: list["LoginSession"] = Relationship(back_populates="user")
    notifications: list["Notification"] = Relationship(back_populates="user")

    # DB constraints for Oracle to restrict values
    __table_args__ = (
        CheckConstraint(
            f"role IN ('{UserRole.ADMIN.value}', '{UserRole.USER.value}')",
            name="check_user_role",
        ),
    )
