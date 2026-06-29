from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    """Schema for creating a new user (admin endpoint)."""

    email: str = Field(min_length=1)
    username: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    title: str = Field(min_length=1)
    password: str = Field(min_length=1)

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    """Schema for updating user information. All fields are optional."""

    email: Optional[str] = Field(default=None, min_length=1)
    username: Optional[str] = Field(default=None, min_length=1)
    display_name: Optional[str] = Field(default=None, min_length=1)
    title: Optional[str] = Field(default=None, min_length=1)
    password: Optional[str] = Field(default=None, min_length=1)

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    """Schema returned to clients when a user object is requested."""

    id: int
    email: Optional[str] = None
    username: Optional[str] = None
    display_name: Optional[str] = None
    title: Optional[str] = None
    role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Auth related schemas (must be in this file per project contract)

