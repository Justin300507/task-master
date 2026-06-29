from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import User
from app.models.lists import List
from app.models.tasks import Task
from app.models.tags import Tag

stats_router = APIRouter()

@stats_router.get("/stats/summary")
def get_summary(db: Session = Depends(get_db)):
    total_users = db.query(User.id).count()
    total_lists = db.query(List.id).count()
    total_tasks = db.query(Task.id).count()
    total_tags = db.query(Tag.id).count()
    return {
        "total_users": total_users,
        "total_lists": total_lists,
        "total_tasks": total_tasks,
        "total_tags": total_tags,
    }
