from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.database import Base

class List(Base):
    __tablename__ = "lists"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
