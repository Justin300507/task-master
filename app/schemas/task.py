from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    tags: Optional[List[str]] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    tags: Optional[List[str]] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    completed: bool = False
    tags: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)
