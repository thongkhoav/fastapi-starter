from enum import Enum
from uuid import uuid4

# from sqlalchemy import Column, Enum as SQLEnum, Integer, String, CheckConstraint
from app.db.base import Base
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(SQLModel, table=True):
    __tablename__ = "users"
    id = Field(default=uuid4, primary_key=True)
    fullName = Field(max_length=100, nullable=False)
    email = Field(max_length=255, unique=True, index=True, nullable=False)
    hashed_password = Field(max_length=255, nullable=False)
    role = Field(default=UserRole.USER.value, nullable=False)

    # DB constraints for Oracle to restrict values
    # __table_args__ = (
    #     CheckConstraint(
    #         f"role IN ('{UserRole.ADMIN.value}', '{UserRole.USER.value}')",
    #         name="check_user_role",
    #     ),
    # )
