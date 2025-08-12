from sqlalchemy.orm import Session
from app.core.environment import Environment
from app.models.user import User, UserRole
from app.schemas.user.user_schema import UserDBCreate
from app.utils import password as pw_util
from datetime import datetime, timedelta, timezone
import jwt


# Load environment variables
read_env = Environment()

# TOKEN CONFIG
ACCESS_TOKEN_SECRET_KEY = read_env.ACCESS_TOKEN_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = read_env.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = read_env.ALGORITHM
REFRESH_TOKEN_SECRET_KEY = read_env.REFRESH_TOKEN_SECRET_KEY
REFRESH_TOKEN_EXPIRE_MINUTES = read_env.REFRESH_TOKEN_EXPIRE_MINUTES


# Handler
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    # Set the expiration time
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": int(expire.timestamp())})
    # Sign the token
    return jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    # Set the expiration time
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": int(expire.timestamp())})
    # Sign the token
    return jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)


def create_user(db: Session, user: UserDBCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    print("create user:", db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()  # type: ignore


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user and pw_util.verify_password(password, user.hashed_password):
        return user
    return None
