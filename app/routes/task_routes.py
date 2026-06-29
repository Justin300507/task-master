from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.tasks import Task
from app.models.tags import Tag
from app.utils.auth import get_current_user, oauth2_scheme
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

# Router variable as required
task_router = APIRouter()

# ---------- Helper Functions ----------
def _get_or_create_tag(db: Session, name: str) -> Tag:
    existing = (
        db.query(Tag)
        .filter(func.lower(Tag.name) == name.lower())
        .first()
    )
    if existing:
        return existing
    new_tag = Tag(name=name)
    db.add(new_tag)
    db.flush()  # ensure id is generated
    return new_tag

def _apply_tag_updates(db: Session, task: Task, tag_names: Optional[List[str]]) -> None:
    if tag_names is None:
        return
    # Normalise tag names (strip whitespace, ignore empties)
    cleaned = [t.strip() for t in tag_names if t and t.strip()]
    existing_tags = {tag.name.lower(): tag for tag in task.tags}
    # Add new tags
    for name in cleaned:
        if name.lower() not in existing_tags:
            tag_obj = _get_or_create_tag(db, name)
            task.tags.append(tag_obj)
    # Remove tags not present in cleaned list
    to_remove = [tag for lname, tag in existing_tags.items() if lname not in [n.lower() for n in cleaned]]
    for tag in to_remove:
        task.tags.remove(tag)

# ---------- Endpoints ----------
@task_router.get("/tasks", response_model=dict)
def get_tasks(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    status: Optional[bool] = Query(None, description="Filter by completed status"),
    due_before: Optional[datetime] = Query(None),
    due_after: Optional[datetime] = Query(None),
    tag_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    query = db.query(Task)

    if status is not None:
        query = query.filter(Task.completed == status)
    if due_before:
        query = query.filter(Task.due_date != None).filter(Task.due_date <= due_before)
    if due_after:
        query = query.filter(Task.due_date != None).filter(Task.due_date >= due_after)
    if tag_id:
        query = query.join(Task.tags).filter(Tag.id == tag_id)

    total = query.count()
    tasks = query.offset(offset).limit(limit).all()

    items = [
        TaskResponse(
            id=t.id,
            title=t.title,
            description=t.description,
            due_date=t.due_date,
            completed=t.completed,
            tags=[tag.name for tag in t.tags],
        ).model_dump()
        for t in tasks
    ]
    return {"items": items, "total": total}

@task_router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        completed=task.completed,
        tags=[tag.name for tag in task.tags],
    )

@task_router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    task = Task(
        title=task_in.title,
        description=task_in.description,
        due_date=task_in.due_date,
        completed=False,
    )
    db.add(task)
    db.flush()  # generate ID before tag association
    if task_in.tags:
        for tag_name in task_in.tags:
            tag_obj = _get_or_create_tag(db, tag_name)
            task.tags.append(tag_obj)
    db.commit()
    db.refresh(task)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        completed=task.completed,
        tags=[tag.name for tag in task.tags],
    )

@task_router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_in: TaskUpdate,
    task_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")

    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.due_date is not None:
        task.due_date = task_in.due_date
    if task_in.completed is not None:
        task.completed = task_in.completed
    if task_in.tags is not None:
        _apply_tag_updates(db, task, task_in.tags)

    db.commit()
    db.refresh(task)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        completed=task.completed,
        tags=[tag.name for tag in task.tags],
    )

@task_router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(task)
    db.commit()
    return Response(status_code=204)

@task_router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_complete(
    task_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    task.completed = not task.completed
    db.commit()
    db.refresh(task)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        completed=task.completed,
        tags=[tag.name for tag in task.tags],
    )