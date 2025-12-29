from fastapi import APIRouter ,Depends
from pydantic import BaseModel
from model import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter()

bcrypt_context  = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role : str

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session , Depends (get_db)]


@router.post("/auth" , status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency ,
                      user_request: CreateUserRequest 
                      ):
    create_user_model = Users(
        username=user_request.username,
        email=user_request.email,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        role = user_request.role,
        is_active = True
    )
    db.add(create_user_model)
    db.commit()
    return create_user_model


