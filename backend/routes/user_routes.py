from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.database import get_db
from backend.models.user_model import User
from pydantic import BaseModel

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed = pwd_context.hash(user.password)
    new_user = User(username=user.username, password=hashed)
    db.add(new_user)
    try:
        db.commit()
        return {"message": "User registered successfully"}
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

@router.get("/all")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()
