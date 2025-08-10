from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserDBCreate

def create_user(db: Session, user: UserDBCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db:Session, skip: int=0, limit:int=10):
    return db.query(User).offset(skip).limit(limit).all()