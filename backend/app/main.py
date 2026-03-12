from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import models, database
from .core import logic
from .db.schemas import AnalysisRequest, AnalysisResponse, HistoryResponse
from typing import List

app = FastAPI(title="TruthLens API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze_content(request: AnalysisRequest, db: Session = Depends(database.get_db)):
    result = logic.calculate_reliability_score(request.content)
    
    # Save to history
    db_analysis = models.AnalysisHistory(
        content=request.content,
        score=result["score"],
        label=result["label"],
        risky_keywords=",".join(result["risky_keywords"]),
        detected_links=",".join(result["links"])
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return {
        "id": db_analysis.id,
        **result,
        "created_at": db_analysis.created_at
    }

@app.get("/api/history", response_model=List[HistoryResponse])
def get_history(db: Session = Depends(database.get_db)):
    history = db.query(models.AnalysisHistory).order_by(models.AnalysisHistory.created_at.desc()).all()
    return history
