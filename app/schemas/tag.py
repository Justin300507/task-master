from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class TagCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)

    model_config = ConfigDict(from_attributes=True)


class TagUpdate(BaseModel):
    title: str = Field(min_length=1)

    model_config = ConfigDict(from_attributes=True)


class TagResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TagListResponse(BaseModel):
    tags: List[TagResponse]

    model_config = ConfigDict(from_attributes=True)
