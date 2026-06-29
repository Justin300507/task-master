from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class TaskTag(Base):
    __tablename__ = "task_tags"
    __table_args__ = {"extend_existing": True}
    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True, nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True, nullable=False)
