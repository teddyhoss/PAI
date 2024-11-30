from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.connection import get_db, Base, engine
from services.classifier import IssueClassifier
from pydantic import BaseModel
from database import models

app = FastAPI()
classifier = IssueClassifier()

# Crea le tabelle nel database
Base.metadata.create_all(bind=engine)

class Issue(BaseModel):
    text: str

@app.post("/classify/")
def classify_issue(issue: Issue, db: Session = Depends(get_db)):
    # Classifica il problema
    classification = classifier.classify_issue(issue.text)
    
    # Salva nel database
    db_issue = models.Issue(
        text=issue.text,
        classification=classification
    )
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    
    return classification

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
