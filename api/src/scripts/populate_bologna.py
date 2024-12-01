import csv
import sys
import os
from pathlib import Path
import logging
from sqlalchemy.orm import Session
sys.path.append(str(Path(__file__).parent.parent))

from database.connection import get_db, engine
from services.classifier import IssueClassifier
from database import models

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_bologna_csv(csv_path: str, db: Session):
    classifier = IssueClassifier()
    success = 0
    errors = 0
    
    logger.info(f"\n🔄 Elaborazione del file {csv_path}...")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            # Leggi il contenuto del file per debug
            content = file.read()
            logger.debug(f"Contenuto del file:\n{content[:500]}...")  # Primi 500 caratteri
            file.seek(0)  # Torna all'inizio
            
            reader = csv.reader(file)
            next(reader)  # Salta l'header
            
            total_rows = sum(1 for row in file)
            file.seek(0)  # Torna all'inizio
            next(reader)  # Salta di nuovo l'header
            
            for i, row in enumerate(reader, 1):
                try:
                    if not row or len(row) < 2:  # Salta righe vuote o malformate
                        logger.warning(f"Riga {i} malformata o vuota: {row}")
                        continue
                        
                    cap = row[0].strip()
                    text = row[1].strip()
                    
                    if not text or not cap:  # Salta se mancano dati essenziali
                        logger.warning(f"Riga {i} con dati mancanti - CAP: {cap}, Testo: {text}")
                        continue
                    
                    logger.info(f"\n📝 Elaborazione riga {i}/{total_rows-1}:")
                    logger.info(f"Testo: {text[:100]}...")
                    logger.info(f"CAP: {cap}")
                    
                    # Classifica il problema
                    classification = classifier.classify_issue(text, cap)
                    
                    # Salva nel database
                    db_issue = models.Issue(
                        text=text,
                        cap=cap,
                        source='bologna_csv',
                        classification=classification
                    )
                    db.add(db_issue)
                    db.commit()
                    
                    logger.info(f"✅ Classificato come: {classification.get('category', 'N/A')} "
                          f"(Urgenza: {classification.get('urgency', 'N/A')})")
                    success += 1
                    
                except Exception as e:
                    logger.error(f"❌ Errore alla riga {i}: {str(e)}")
                    logger.exception("Dettaglio errore:")
                    errors += 1
                    db.rollback()
                    continue
                    
    except Exception as e:
        logger.error(f"❌ Errore nella lettura del file: {str(e)}")
        logger.exception("Dettaglio errore:")
        raise
    
    return success, errors

def main():
    csv_path = os.path.join(Path(__file__).parent, 'bologna.csv')
    if not os.path.exists(csv_path):
        logger.error(f"❌ File non trovato: {csv_path}")
        sys.exit(1)
    
    logger.info("\n🚀 Avvio popolazione database da CSV Bologna...")
    
    try:
        db = next(get_db())
        success, errors = process_bologna_csv(csv_path, db)
        
        logger.info("\n📊 Riepilogo:")
        logger.info(f"✅ Proposte elaborate con successo: {success}")
        logger.info(f"❌ Errori: {errors}")
        
    except Exception as e:
        logger.error(f"\n❌ Errore critico: {str(e)}")
        logger.exception("Traceback completo:")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main() 