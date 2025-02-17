from pydantic import BaseModel
from typing import Optional, List

class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(Todo):
    user_id: int

class TodoResponse(Todo):
    id: int
    user_id: int
    class Config: 
        from_attributes = True

class Userbase(BaseModel):
    name: str
    email: str

class UserCreate(Userbase):
    password: str

class Token(BaseModel):
    access_token: str
    access_type: str

class UserResponse(Userbase):
    id: int
    todos: List[TodoResponse] = []
    class Config:
        from_attributes = True
    