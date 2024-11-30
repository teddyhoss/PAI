from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database.connection import get_db, Base, engine
from services.classifier import IssueClassifier
from pydantic import BaseModel
from database import models
import csv
import io
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
os.makedirs("src/static/images", exist_ok=True)

# Copia il logo nella cartella static/images se non è già presente
if not os.path.exists("src/static/images/TalkNow.png"):
    shutil.copy("TalkNow.png", "src/static/images/TalkNow.png")

# Monta la cartella static
app.mount("/static", StaticFiles(directory="src/static"), name="static")

class Issue(BaseModel):
    text: str
    cap: str

class IssueResponse(BaseModel):
    id: int
    text: str
    cap: str
    classification: dict
    timestamp: datetime

@app.post("/classify/", response_model=IssueResponse)
def classify_issue(issue: Issue, db: Session = Depends(get_db)):
    # Classifica il problema
    classification = classifier.classify_issue(issue.text)
    
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

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        buffer = io.StringIO(contents.decode())
        csv_reader = csv.DictReader(buffer)
        
        processed = 0
        errors = []
        
        for row in csv_reader:
            try:
                if 'text' not in row or 'cap' not in row:
                    raise ValueError(f"Riga mancante di campi obbligatori: {row}")
                
                classification = classifier.classify_issue(row['text'])
                
                db_issue = models.Issue(
                    text=row['text'],
                    cap=row['cap'],
                    source='csv',
                    classification=classification
                )
                db.add(db_issue)
                processed += 1
                
            except Exception as e:
                errors.append(f"Errore alla riga {processed + 1}: {str(e)}")
        
        db.commit()
        
        return {
            "success": True,
            "processed": processed,
            "errors": errors
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(models.Issue).count()
    by_category = db.query(models.Issue.classification['category'].label('category'), 
                          func.count('*').label('count'))\
                    .group_by('category').all()
    
    return {
        "total": total,
        "by_category": [{"category": c[0], "count": c[1]} for c in by_category]
    }

@app.get("/api/check-logo")
def check_logo():
    logo_path = "src/static/images/TalkNow.png"
    return {
        "exists": os.path.exists(logo_path),
        "size": os.path.getsize(logo_path) if os.path.exists(logo_path) else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
