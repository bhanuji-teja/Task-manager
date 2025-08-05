from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.task_model import Task
from pydantic import BaseModel
from typing import List

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    user_id: int

@router.post("/create")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    return {"message": "Task created successfully"}

@router.get("/tasks/")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.get("/user/{user_id}")
def get_user_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks
