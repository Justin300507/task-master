from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.database import Base

class ListMember(Base):
    __tablename__ = "list_members"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)
    added_at = Column(DateTime, server_default=func.now(), nullable=False)
