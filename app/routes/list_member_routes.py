from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.list_members import ListMember
from app.models.users import User
from app.utils.auth import get_current_user, oauth2_scheme
from app.schemas.list_member import ListMemberCreate, ListMemberUpdate, ListMemberRead

list_member_router = APIRouter()

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def _get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def _get_list_member(db: Session, member_id: int) -> ListMember:
    member = db.query(ListMember).filter(ListMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="List member not found")
    return member

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@list_member_router.get("/list_members", response_model=dict)
def list_members(
    list_id: Optional[int] = Query(None, ge=1),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: str = Depends(oauth2_scheme),
):
    """List members of a list, optionally filtered by ``list_id``.
    Returns ``{"items": [...], "total": <int>}``.
    """
    query = db.query(ListMember)
    if list_id is not None:
        query = query.filter(ListMember.list_id == list_id)

    total = query.count()
    members = query.offset(offset).limit(limit).all()

    items: List[dict] = []
    for member in members:
        user = (
            member.user
            if hasattr(member, "user") and member.user is not None
            else db.query(User).filter(User.id == member.user_id).first()
        )
        items.append(
            {
                "id": member.id,
                "list_id": member.list_id,
                "user_id": member.user_id,
                "email": user.email if user else None,
                "role": getattr(member, "role", None),
            }
        )

    return {"items": items, "total": total}


@list_member_router.get("/list_members/{member_id}", response_model=ListMemberRead)
def get_list_member(
    member_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: str = Depends(oauth2_scheme),
):
    member = _get_list_member(db, member_id)
    user = db.query(User).filter(User.id == member.user_id).first()
    return ListMemberRead(
        id=member.id,
        list_id=member.list_id,
        user_id=member.user_id,
        email=user.email if user else None,
        role=getattr(member, "role", None),
    )


@list_member_router.post("/list_members", response_model=ListMemberRead, status_code=201)
def create_list_member(
    payload: ListMemberCreate,
    db: Session = Depends(get_db),
    _: str = Depends(oauth2_scheme),
):
    # Verify the list exists - rely on FK constraint; will raise IntegrityError if invalid
    user = _get_user_by_email(db, payload.email)

    # Prevent duplicate membership
    existing = (
        db.query(ListMember)
        .filter(ListMember.list_id == payload.list_id, ListMember.user_id == user.id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="User already a member of the list")

    new_member = ListMember(
        list_id=payload.list_id,
        user_id=user.id,
        role=payload.role,
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return ListMemberRead(
        id=new_member.id,
        list_id=new_member.list_id,
        user_id=new_member.user_id,
        email=user.email,
        role=getattr(new_member, "role", None),
    )


@list_member_router.put("/list_members/{member_id}", response_model=ListMemberRead)
def update_list_member(
    payload: ListMemberUpdate,
    member_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: str = Depends(oauth2_scheme),
):
    member = _get_list_member(db, member_id)
    member.role = payload.role
    db.commit()
    db.refresh(member)
    user = db.query(User).filter(User.id == member.user_id).first()
    return ListMemberRead(
        id=member.id,
        list_id=member.list_id,
        user_id=member.user_id,
        email=user.email if user else None,
        role=getattr(member, "role", None),
    )


@list_member_router.delete("/list_members/{member_id}", status_code=204)
def delete_list_member(
    member_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: str = Depends(oauth2_scheme),
):
    member = _get_list_member(db, member_id)
    db.delete(member)
    db.commit()
    return None
