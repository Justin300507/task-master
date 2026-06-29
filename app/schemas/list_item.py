from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ListItemCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)

class ListItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)

class ListItemResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

