from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from database import get_db
import models
import schemas

router = APIRouter(tags = ["Authentication"])

SECRET_KEY = "b543da5fe5a0e5080b7bf9a5b541433a217ef1dc0dc4c0f0cb3689de5219d0e1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode["sub"] = str(to_encode["sub"])
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password) 


def get_password_hash(password):
    return bcrypt_context.hash(password)  


@router.post("/users", response_model=schemas.UserResponse, tags = ["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token", response_model=schemas.Token, tags = ["Authentication"])
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.name == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "access_type": "bearer"}


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)): 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials"
    )

    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        user_id = int(user_id)

        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise credentials_exception
        
        return user

    except JWTError:
        raise credentials_exception

