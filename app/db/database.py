from app.core.config import settings

# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from app.core.config import DatabaseConfig

db_instance = DatabaseConfig()


def get_db_session():
    db = next(db_instance.get_session())
    try:
        yield db
    finally:
        db.close()
