from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    score = Column(Integer)
    label = Column(String)
    risky_keywords = Column(Text)  # Comma separated
    detected_links = Column(Text)   # Comma separated
    created_at = Column(DateTime, default=datetime.utcnow)
