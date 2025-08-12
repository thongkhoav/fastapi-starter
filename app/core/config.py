import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

from app.core.environment import Environment

read_env = Environment()


class DatabaseConfig:
    def __init__(self):
        PG_USER: str = read_env.PG_USER
        PG_PASSWORD: str = read_env.PG_PASSWORD
        PG_HOST: str = read_env.PG_HOST
        PG_PORT: int = read_env.PG_PORT
        PG_DATABASE: str = read_env.PG_DATABASE

        # Database URL
        self.DATABASE_URL = f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
        print("database url" + self.DATABASE_URL)

        # Create the database engine
        self.engine = create_engine(self.DATABASE_URL, echo=True)

    def create_db_and_tables(self):
        # Import models here to avoid circular imports
        from app.models.user import User
        from app.models.room import Room
        from app.models.task import Task
        from app.models.user_room import UserRoom
        from app.models.notification import Notification
        from app.models.login_session import LoginSession

        # Create tables
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        # Function to get a database session
        with Session(self.engine) as session:
            yield session

    def drop_db(self):
        SQLModel.metadata.drop_all(self.engine)
