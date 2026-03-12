from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AnalysisRequest(BaseModel):
    content: str

class AnalysisResponse(BaseModel):
    id: int
    score: int
    label: str
    risky_keywords: List[str]
    links: List[str]
    created_at: datetime

class HistoryResponse(BaseModel):
    id: int
    content: str
    score: int
    label: str
    risky_keywords: str
    detected_links: str
    created_at: datetime

    class Config:
        from_attributes = True
