from pydantic import BaseModel
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoResponse(TodoCreate):
    id: int

    model_config = {"from_attributes": True}
    