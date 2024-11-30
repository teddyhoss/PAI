from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from services.classifier import IssueClassifier
from pydantic import BaseModel

app = FastAPI()
classifier = IssueClassifier()

class Issue(BaseModel):
    text: str

@app.post("/classify/")
async def classify_issue(issue: Issue, db: Session = Depends(get_db)):
    # Classifica il problema
    classification = await classifier.classify_issue(issue.text)
    
    # Qui puoi aggiungere la logica per salvare nel database
    # Per esempio:
    # db_issue = models.Issue(
    #     text=issue.text,
    #     classification=classification
    # )
    # db.add(db_issue)
    # db.commit()
    
    return classification

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
