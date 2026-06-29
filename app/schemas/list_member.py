from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ListMemberCreate(BaseModel):
    """Schema for adding a user to a list as a collaborator."""
    list_id: int = Field(..., ge=1)
    email: str = Field(..., min_length=1)
    role: Optional[str] = Field(default="collaborator", min_length=1)


class ListMemberUpdate(BaseModel):
    """Schema for updating a member's role."""
    role: str = Field(..., min_length=1)


class ListMemberResponse(BaseModel):
    id: int
    list_id: Optional[int] = None
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ListMemberRead(BaseModel):
    """Schema for reading a list member's details."""
    id: int
    list_id: int
    user_id: int
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)
