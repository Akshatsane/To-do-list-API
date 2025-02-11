from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models 
import schemas
from database import engine, get_db
from typing import List


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="USER API")

@app.post("/todos", response_model=schemas.TodoResponse)
def create_todos(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == todo.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/todos/{todo_id}", response_model = schemas.TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code = 404, detail = "task cannot be found")
    return todo

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}",response_model = schemas.Userbase)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    user_details = db.query(models.User).filter(models.User.id == user_id).first()
    if user_details is None:
        raise HTTPException(status_code = 404, detail = "user not found")
    return user_details
@app.get("/users/{user_id}/todos", response_model=List[schemas.TodoResponse])
def get_user_todos(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.todos

