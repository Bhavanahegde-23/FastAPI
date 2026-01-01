from fastapi import APIRouter ,Depends
from pydantic import BaseModel
from model import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta , timezone
from .auth import get_current_user

router = APIRouter(
        prefix ='/user',
    tags = ['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session , Depends (get_db)]
user_dependency = Annotated[dict , Depends(get_current_user)]
bcrypt_context  = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Endpoint to get current user details
@router.get('/' , status_code=status.HTTP_200_OK)
async def get_user(db:db_dependency,
                   user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid user")
    return db.query(Users).filter(Users.id == user.get('id')).first()

 #Change password endpoint
class ChangePasswordRequest (BaseModel):
    old_password : str
    new_password : str

@router.put('/password' , status_code=status.HTTP_200_OK)
async def change_password(change_password_request:ChangePasswordRequest,
                            db:db_dependency,
                            user:user_dependency):
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid user")
        
        user_model = db.query(Users).filter(Users.id == user.get('id')).first()
        if not bcrypt_context.verify(change_password_request.old_password , user_model.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Old password is incorrect")
        
        user_model.hashed_password = bcrypt_context.hash(change_password_request.new_password)
        db.add(user_model)
        db.commit()
        return {'detail':'Password changed successfully'}

@router.put('/phone' , status_code=status.HTTP_200_OK)
async def update_phone(phone_no:str,
                            db:db_dependency,
                            user:user_dependency):
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid user")
        
        user_model = db.query(Users).filter(Users.id == user.get('id')).first()
        user_model.phone_no = phone_no
        db.add(user_model)
        db.commit()
        return {'detail':'Phone number updated successfully'}