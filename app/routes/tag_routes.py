from fastapi import APIRouter, Depends, HTTPException, Query, Path, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.tags import Tag
from app.schemas.tag import TagCreate, TagUpdate, TagResponse, TagListResponse

tag_router = APIRouter()

@tag_router.get("/tags", response_model=TagListResponse)
def list_tags(
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(Tag)
    if search:
        query = query.filter(Tag.name.ilike(f"%{search}%"))
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return {"items": items, "total": total}

@tag_router.get("/tags/{tag_id}", response_model=TagResponse)
def get_tag(
    tag_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Not found")
    return tag

@tag_router.post("/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_in: TagCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(Tag).filter(Tag.name == tag_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag with this name already exists")
    tag = Tag(name=tag_in.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

@tag_router.put("/tags/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_in: TagUpdate,
    tag_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Not found")
    tag.name = tag_in.name
    db.commit()
    db.refresh(tag)
    return tag

@tag_router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(tag)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
