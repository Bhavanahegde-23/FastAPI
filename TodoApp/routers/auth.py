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

router = APIRouter()

# Security settings using JWT
SECRET_KEY = '9bd034b43e3976c04b127e5d296d22d091e8b4fa6135fb6928ab76989f25a79e'
ALGORITHM = 'HS256'

bcrypt_context  = CryptContext(schemes=["bcrypt"], deprecated="auto")

#this can be used to secure endpoints
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role : str

class Token(BaseModel):
    access_token:str
    token_type:str

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session , Depends (get_db)]

def authUser(username:str , password:str , db:Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password , user.hashed_password):
        return False
    return user

def create_access_token(username: str , user_id:int , expires_delta:timedelta):
    encode = {'sub': username , 'id':user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode , SECRET_KEY , algorithm=ALGORITHM)

async def get_current_user(token :Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        if username is None or user_id is None:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Could not validate credentials")
        return {'username': username , 'id':user_id}
    except JWTError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Could not validate credentials")

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

@router.post("/token" , response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm , Depends()],
                                 db:db_dependency):
    user = authUser(form_data.username , form_data.password , db)
    if not user:
        return {"error": "Invalid Credentials"}
    token = create_access_token(user.username , user.id , timedelta(minutes=30))
    return {'access_token': token , 'token_type':'bearer'}


