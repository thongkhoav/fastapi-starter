from passlib.context import CryptContext
from app.crud import user_crud
from app.schemas.user_schema import UserCreate, UserDBCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user_data: UserCreate):
    hashed_password = pwd_context.hash(user_data.password)
    user_create: UserDBCreate = UserDBCreate(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )
    return user_crud.create_user(user_create)