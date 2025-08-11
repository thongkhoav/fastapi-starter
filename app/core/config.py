import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

load_dotenv()


class DatabaseConfig:
    def __init__(self):
        ORACLE_USER: str = os.getenv("ORACLE_USER")
        ORACLE_PASSWORD: str = os.getenv("ORACLE_PASSWORD")
        ORACLE_HOST: str = os.getenv("ORACLE_HOST")
        ORACLE_PORT: str = os.getenv("ORACLE_PORT")
        ORACLE_SERVICE_NAME: str = os.getenv("ORACLE_SERVICE_NAME")
        ORACLE_ROLE: str = os.getenv("ORACLE_ROLE", "SYSDBA")

        # Database URL
        self.DATABASE_URL = f"oracle+oracledb://{self.ORACLE_USER}:{self.ORACLE_PASSWORD}@{self.ORACLE_HOST}:{self.ORACLE_PORT}/?service_name={self.ORACLE_SERVICE_NAME}&mode={self.ORACLE_ROLE}"

        # Create the database engine
        self.engine = create_engine(self.DATABASE_URL, echo=True)

    def create_db_and_tables(self):
        # Import models here to avoid circular imports
        from models.user import User

        # from models.book import Book
        # from models.category import Category
        # from models.author import Author
        # from models.order import Order
        # from models.order_item import OrderItem
        # from models.review import Review
        # from models.discount import Discount

        # Create tables
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        # Function to get a database session
        with Session(self.engine) as session:
            yield session

    def drop_db(self):
        SQLModel.metadata.drop_all(self.engine)
