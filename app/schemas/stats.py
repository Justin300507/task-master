from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class StatsCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    model_config = ConfigDict(from_attributes=True)

class StatsUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    model_config = ConfigDict(from_attributes=True)

class StatsResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# Auth schemas

