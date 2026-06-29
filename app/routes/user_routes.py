from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional

from app.database import get_db
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate

user_router = APIRouter()

@user_router.get("/users", response_model=dict)
def list_users(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """List users with optional search and pagination.
    Returns a JSON object {"items": [...], "total": <int>}.
    """
    base_query = db.query(User)
    if search:
        pattern = f"%{search}%"
        base_query = base_query.filter(
            or_(User.email.ilike(pattern), User.username.ilike(pattern), User.display_name.ilike(pattern))
        )
    total = base_query.count()
    users = base_query.offset(offset).limit(limit).all()
    items = [
        {
            "id": u.id,
            "email": u.email,
            "username": getattr(u, "username", None),
            "display_name": getattr(u, "display_name", None),
            "title": getattr(u, "title", None),
        }
        for u in users
    ]
    return {"items": items, "total": total}

@user_router.get("/users/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve details of a specific user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "email": user.email,
        "username": getattr(user, "username", None),
        "display_name": getattr(user, "display_name", None),
        "title": getattr(user, "title", None),
    }

@user_router.post("/users", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Create a new user (admin endpoint)."""
    # Basic uniqueness check for email and username
    existing = (
        db.query(User)
        .filter(or_(User.email == user_in.email, User.username == user_in.username))
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Email or username already exists")
    new_user = User(
        email=user_in.email, full_name=user_in.display_name, title=getattr(user_in, "title", None),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
        "display_name": new_user.display_name,
        "title": getattr(new_user, "title", None),
    }

@user_router.put("/users/{user_id}", response_model=dict)
def update_user(
    user_in: UserUpdate,
    user_id: int,
    db: Session = Depends(get_db),
):
    """Update an existing user's information."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Update only provided fields
    if user_in.email is not None:
        # Ensure email uniqueness
        if (
            db.query(User)
            .filter(User.email == user_in.email, User.id != user_id)
            .first()
        ):
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = user_in.email
    if user_in.username is not None:
        if (
            db.query(User)
            .filter(User.username == user_in.username, User.id != user_id)
            .first()
        ):
            raise HTTPException(status_code=400, detail="Username already in use")
        user.username = user_in.username
    if user_in.display_name is not None:
        user.display_name = user_in.display_name
    if hasattr(user_in, "title") and user_in.title is not None:
        user.title = user_in.title
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "display_name": user.display_name,
        "title": getattr(user, "title", None),
    }

@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None
