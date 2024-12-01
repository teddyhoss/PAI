from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.connection import get_db, Base, engine
from services.classifier import IssueClassifier
from pydantic import BaseModel
from database import models
from datetime import datetime
from sqlalchemy import func
import logging
import uvicorn
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import String
from groq import Groq
from toolhouse import Toolhouse
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TellNow")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelli Pydantic
class Issue(BaseModel):
    text: str
    cap: str

class IssueResponse(BaseModel):
    id: int
    text: str
    cap: str
    classification: dict
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Inizializza il classifier
classifier = None

# Inizializzazione di Groq e Toolhouse con le chiavi dall'env
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
th = Toolhouse(api_key=os.getenv('TOOLHOUSE_KEY', 'th-tmKDVLNhiv0uXzH5CKMDZaZTqi57fWexf61FD9KaD14'))
MODEL = "llama3-groq-70b-8192-tool-use-preview"

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    try:
        # Conteggio totale
        total = db.query(models.Issue).count()

        # Conteggio urgenza alta
        high_urgency_count = db.query(models.Issue).filter(
            models.Issue.classification['urgency'].cast(String) == 'high'
        ).count()

        # Distribuzione per categoria
        categories_query = db.query(
            models.Issue.classification['category'].cast(String),
            func.count('*')
        ).group_by(
            models.Issue.classification['category'].cast(String)
        ).all()

        categories_distribution = {}
        for cat in categories_query:
            if cat[0] is not None:
                # Rimuove le virgolette extra dal JSON
                clean_cat = cat[0].strip('"') if cat[0] else None
                categories_distribution[clean_cat] = cat[1]

        # Distribuzione per CAP
        zones_query = db.query(
            models.Issue.cap,
            func.count('*')
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
                "city": issue.classification.get("city"),
                "coordinates": issue.classification.get("coordinates"),
                "timestamp": issue.timestamp
            } for issue in recent_issues]
        }
    except Exception as e:
        logger.error(f"Errore in get_stats: {str(e)}")
        logger.exception("Traceback completo:")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/check")
async def check():
    return {"status": "ok"}

@app.post("/api/classify/")
async def classify_issue(issue: Issue, db: Session = Depends(get_db)):
    global classifier
    
    try:
        # Inizializza il classifier solo al primo utilizzo
        if classifier is None:
            logger.info("Inizializzazione classifier...")
            classifier = IssueClassifier()
            logger.info("Classifier inizializzato")

        # Classifica
        classification = classifier.classify_issue(issue.text, issue.cap)
        
        if not classification.get("valid", False):
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Segnalazione non valida",
                    "original_text": issue.text,
                    "reason": classification.get("reason", "Motivo non specificato")
                }
            )

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
        
        return {
            "id": db_issue.id,
            "text": db_issue.text,
            "cap": db_issue.cap,
            "classification": db_issue.classification,
            "timestamp": db_issue.timestamp
        }
        
    except Exception as e:
        logger.error(f"Errore in classify_issue: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.post("/api/chat")
async def chat(request: dict):
    try:
        # Prepara il messaggio di sistema con il contesto
        messages = request['messages']
        
        # Prima chiamata per ottenere la risposta iniziale
        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=th.get_tools(),
            temperature=0.3,  # Aggiungiamo temperatura più bassa per risposte più precise
        )

        # Estrai la risposta iniziale
        assistant_message = response.choices[0].message
        
        # Aggiungi la risposta dell'assistente ai messaggi
        messages.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": assistant_message.tool_calls if hasattr(assistant_message, 'tool_calls') else None
        })

        # Esegui gli strumenti se necessario
        tool_run = th.run_tools(response)
        if tool_run:
            # Aggiungi i risultati degli strumenti ai messaggi
            messages.extend(tool_run)
            
            # Ottieni la risposta finale dopo l'esecuzione degli strumenti
            final_response = groq_client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=th.get_tools(),
                temperature=0.3,
            )
            
            # Usa la risposta finale
            final_content = final_response.choices[0].message.content
            logger.info(f"Risposta finale dopo tool execution: {final_content}")
            return {"response": final_content}
        
        # Se non ci sono tool da eseguire, usa la risposta iniziale
        logger.info(f"Risposta senza tool execution: {assistant_message.content}")
        return {"response": assistant_message.content}

    except Exception as e:
        logger.error(f"Errore nella chat: {str(e)}")
        logger.exception("Traceback completo:")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    try:
        logger.info("Creazione tabelle database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelle database create con successo")
    except Exception as e:
        logger.error(f"Errore nella creazione delle tabelle: {e}")

    logger.info("Avvio server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
