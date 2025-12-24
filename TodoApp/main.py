from fastapi import FastAPI , Depends , Path
import model
from database import engine , SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from model import Todos
from fastapi import HTTPException
from starlette import status
from pydantic import BaseModel , Field



app =FastAPI()

#creates the database tables
model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session , Depends (get_db)]

class TodoRequest(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length=3 , max_length=100)
    priority:int = Field(gt=0 , lt=6)
    complete:bool 


@app.get("/")
async def read_all(db:db_dependency , status_code = status.HTTP_200_OK):
    todos = db.query(Todos).all()
    return todos

@app.get('/todo/{todo_id}' , status_code=status.HTTP_200_OK)
async def read_todo(db : db_dependency , todo_id : int = Path (gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404 , detail = "Todo not found")

@app.post("/todo/" , status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency ,todo_request:TodoRequest):
    todo_model =Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()
    return todo_model

@app.put("/todo/{todo_id}" , status_code=status.HTTP_200_OK)
async def update_todo(db:db_dependency ,
                      todo_request:TodoRequest,
                      todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404 , detail = "Todo not found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

    return todo_model


@app.delete("/todo/{todo_id}" , status_code=status.HTTP_200_OK)
async def delete_todo(db:db_dependency , todo_id:int = Path (gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404 , detail = "Todo not found")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    return {"detail":"Todo deleted successfully"}



