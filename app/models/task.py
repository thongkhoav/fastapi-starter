from enum import Enum
from uuid import uuid4

from sqlalchemy import CheckConstraint
from typing import TYPE_CHECKING, Optional
from datetime import date
from sqlmodel import Field, SQLModel, Relationship, String, Column

if TYPE_CHECKING:
    from .user_room import UserRoom
    from .user import User
    from .room import Room


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(SQLModel, table=True):
    __tablename__ = "tasks"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String(255), nullable=False))
    description: Optional[str] = Field(sa_column=Column(String(1000), nullable=True))
    due_date: date = Field(default=date.today, nullable=False)
    status: TaskStatus = Field(
        default=TaskStatus.TODO, sa_column=Column(String(20), nullable=False)
    )
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    room_id: Optional[int] = Field(default=None, foreign_key="rooms.id")

    # Relationships
    user: Optional["User"] = Relationship(
        back_populates="tasks"
    )  # back_populates tasks because user model has tasks relationship
    room: Optional["Room"] = Relationship(
        back_populates="tasks"
    )  # back_populates tasks because room model has tasks relationship

    # DB constraints for Oracle to restrict values
    __table_args__ = (
        CheckConstraint(
            f"status IN ('{TaskStatus.TODO.value}', '{TaskStatus.IN_PROGRESS.value}', '{TaskStatus.DONE.value}')",
            name="check_task_status",
        ),
    )
