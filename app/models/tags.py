from sqlalchemy import Column, Integer, String
from app.database import Base

class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

