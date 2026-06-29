from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.lists import List
from app.schemas.list_item import ListItemCreate, ListItemUpdate
from app.utils.auth import get_current_user

# Router variable must be named exactly as required
list_item_router = APIRouter()

# ---------------------------------------------------------------------------
# GET /lists - list task lists with optional search, owner filter and pagination
# ---------------------------------------------------------------------------
@list_item_router.get("/lists", response_model=dict)
def get_lists(
    search: Optional[str] = Query(None, description="Search by list name"),
    owner_id: Optional[int] = Query(None, ge=1, description="Filter by owner user id"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(List)
    if search:
        query = query.filter(List.name.ilike(f"%{search}%"))
    if owner_id is not None:
        # Assume List model has an "owner_id" FK to users.id
        query = query.filter(List.owner_id == owner_id)
    total = query.count()
    lists = query.offset(offset).limit(limit).all()
    items = []
    for lst in lists:
        item = {
            "id": lst.id,
            "name": getattr(lst, "name", None),
            "owner_id": getattr(lst, "owner_id", None),
        }
        # Include description if the column exists
        if hasattr(lst, "description"):
            item["description"] = lst.description
        items.append(item)
    return {"items": items, "total": total}

# ---------------------------------------------------------------------------
# GET /lists/{id} - get details of a specific task list
# ---------------------------------------------------------------------------
@list_item_router.get("/lists/{id}", response_model=dict)
def get_list(
    id: int,
    db: Session = Depends(get_db),
):
    lst = db.query(List).filter(List.id == id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Not found")
    result = {
        "id": lst.id,
        "name": getattr(lst, "name", None),
        "owner_id": getattr(lst, "owner_id", None),
    }
    if hasattr(lst, "description"):
        result["description"] = lst.description
    return result

# ---------------------------------------------------------------------------
# POST /lists - create a new task list (authenticated)
# ---------------------------------------------------------------------------
@list_item_router.post("/lists", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_list(
    list_in: ListItemCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    # Create a new List instance. The List model is expected to have a
    # "name" (or "title") column and optionally a "description" column.
    new_list = List(
        name=list_in.title,
        owner_id=getattr(current_user, "id", None),
    )
    # If the List model defines a description column, set it.
    if hasattr(new_list, "description") and getattr(list_in, "description", None) is not None:
        new_list.description = list_in.description
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    result = {
        "id": new_list.id,
        "name": getattr(new_list, "name", None),
        "owner_id": getattr(new_list, "owner_id", None),
    }
    if hasattr(new_list, "description"):
        result["description"] = new_list.description
    return result

# ---------------------------------------------------------------------------
# PUT /lists/{id} - update list name or metadata (authenticated, owner only)
# ---------------------------------------------------------------------------
@list_item_router.put("/lists/{id}", response_model=dict)
def update_list(
    list_in: ListItemUpdate,
    id: int,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    lst = db.query(List).filter(List.id == id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Not found")
    # Owner‑only check
    if getattr(lst, "owner_id", None) != getattr(current_user, "id", None):
        raise HTTPException(status_code=403, detail="Forbidden")
    if list_in.title is not None:
        lst.name = list_in.title
    if hasattr(lst, "description") and getattr(list_in, "description", None) is not None:
        lst.description = list_in.description
    db.commit()
    db.refresh(lst)
    result = {
        "id": lst.id,
        "name": getattr(lst, "name", None),
        "owner_id": getattr(lst, "owner_id", None),
    }
    if hasattr(lst, "description"):
        result["description"] = lst.description
    return result

# ---------------------------------------------------------------------------
# DELETE /lists/{id} - delete a task list (authenticated, owner only)
# ---------------------------------------------------------------------------
@list_item_router.delete("/lists/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(
    id: int,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    lst = db.query(List).filter(List.id == id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Not found")
    # Owner‑only check
    if getattr(lst, "owner_id", None) != getattr(current_user, "id", None):
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(lst)
    db.commit()
    return None
