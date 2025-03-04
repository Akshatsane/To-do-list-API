from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(50), index=True)
    description = Column(String(255), index=True)
    completed = Column(Boolean, default=False)  

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todos")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(100), nullable = False)
    email = Column(String(255), nullable = False)
    hashed_password = Column(String(255), nullable = False)
    disabled = Column(Boolean, default = False)

    todos = relationship("Todo", back_populates="owner")

    