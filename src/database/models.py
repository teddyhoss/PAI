from sqlalchemy import Column, Integer, String, JSON, DateTime, Enum
from sqlalchemy.sql import func
from .connection import Base
import enum

class ZoneType(enum.Enum):
    residential = "residential"
    commercial = "commercial"
    industrial = "industrial"
    public_space = "public_space"

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    cap = Column(String(5), nullable=False)
    source = Column(String, default='web')
    classification = Column(JSON, nullable=False)
    zone_type = Column(Enum(ZoneType))
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) 