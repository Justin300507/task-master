from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class SeedCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    notes: Optional[str] = None

class SeedUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None

class SeedResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

