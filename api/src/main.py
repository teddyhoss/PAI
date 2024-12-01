from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database.connection import get_db, Base, engine
from services.classifier import IssueClassifier
from pydantic import BaseModel
from database import models
from datetime import datetime
from typing import Optional
from sqlalchemy import func
import os

app = FastAPI(title="TellNow")
classifier = IssueClassifier()

# Crea le tabelle nel database
Base.metadata.create_all(bind=engine)

# Sposta il logo nella cartella static
import shutil
import os

# Crea la cartella images se non esiste
# os.makedirs("src/static/images", exist_ok=True)

# Copia il logo nella cartella static/images se non è già presente
# if not os.path.exists("src/static/images/TalkNow.png"):
#     shutil.copy("TalkNow.png", "src/static/images/TalkNow.png")

# Monta la cartella static
# app.mount("/static", StaticFiles(directory="src/static"), name="static")

class Issue(BaseModel):
    text: str
    cap: str

class IssueResponse(BaseModel):
    id: int
    text: str
    cap: str
    classification: dict
    timestamp: datetime

@app.post("/api/classify/", response_model=IssueResponse)
def classify_issue(issue: Issue, db: Session = Depends(get_db)):
    try:
        # Classifica il problema
        classification = classifier.classify_issue(issue.text, issue.cap)
        
        # Salva nel database
        db_issue = models.Issue(
            text=issue.text,
            cap=issue.cap,
            source='web',
            classification=classification
        )
        db.add(db_issue)
        db.commit()
        db.refresh(db_issue)
        
        return IssueResponse(
            id=db_issue.id,
            text=db_issue.text,
            cap=db_issue.cap,
            classification=db_issue.classification,
            timestamp=db_issue.timestamp
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    try:
        # Totale segnalazioni
        total = db.query(models.Issue).count()
        
        # Conteggio per urgenza alta usando sintassi PostgreSQL corretta
        high_urgency_count = db.query(models.Issue)\
            .filter(models.Issue.classification['urgency'] == "high")\
            .count()
        
            
        # Distribuzione per categoria
        categories_query = db.query(
            models.Issue.classification['category'],
            func.count('*').label('count')
        ).group_by(models.Issue.classification['category']).all()
        
        categories_distribution = {}
        for cat in categories_query:
            if cat[0] is not None:
                categories_distribution[cat[0]] = cat[1]
        
        # Distribuzione per CAP
        zones_query = db.query(
            models.Issue.cap,
            func.count('*').label('count')
        ).group_by(models.Issue.cap).all()
        
        zones_distribution = {zone: count for zone, count in zones_query}
        
        # Categoria più frequente
        top_category = max(categories_distribution.items(), key=lambda x: x[1])[0] if categories_distribution else None
        
        # CAP più frequente
        top_zone = max(zones_distribution.items(), key=lambda x: x[1])[0] if zones_distribution else None
        
        # Ultime 10 segnalazioni
        recent_issues = db.query(models.Issue)\
            .order_by(models.Issue.timestamp.desc())\
            .limit(10)\
            .all()
        
        return {
            "total": total,
            "high_urgency_count": high_urgency_count,
            "top_category": top_category,
            "top_zone": top_zone,
            "categories_distribution": categories_distribution,
            "zones_distribution": zones_distribution,
            "recent_issues": [{
                "id": issue.id,
                "text": issue.text,
                "cap": issue.cap,
                "category": issue.classification.get("category"),
                "urgency": issue.classification.get("urgency"),
                "explanation": issue.classification.get("explanation"),
                "timestamp": issue.timestamp
            } for issue in recent_issues]
        }
    except Exception as e:
        print(f"Errore in get_stats: {str(e)}")  # Debug log
        return {"error": str(e)}

# @app.get("/api/check-logo")
# def check_logo():
#     logo_path = "src/static/images/TalkNow.png"
#     return {
#         "exists": os.path.exists(logo_path),
#         "size": os.path.getsize(logo_path) if os.path.exists(logo_path) else 0
#     }

@app.get("/api/check")
def check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
