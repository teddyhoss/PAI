from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from .connection import Base

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    cap = Column(String(5), nullable=False)
    source = Column(String, default='web')
    classification = Column(JSON, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) 