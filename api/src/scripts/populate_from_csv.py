import csv
import sys
import os
from pathlib import Path
import random
from sqlalchemy.orm import Session
sys.path.append(str(Path(__file__).parent.parent))

from database.connection import get_db, engine
from services.classifier import IssueClassifier
from database import models

# Lista di CAP di esempio per test
TEST_CAPS = [
    "00118",  # Roma - EUR
    "00121",  # Roma - Prati
    "00127",  # Roma - Torrino
    "00131",  # Roma - Talenti
    "00136",  # Roma - Monte Mario
    "00142",  # Roma - Montagnola
    "00144",  # Roma - EUR Mostacciano
    "00145",  # Roma - Portuense
    "00151",  # Roma - Monteverde
    "00153",  # Roma - Trastevere
]

def process_csv(csv_path: str, db: Session):
    classifier = IssueClassifier()
    success = 0
    errors = 0
    
    print(f"\n🔄 Elaborazione del file {csv_path}...")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        total_rows = sum(1 for row in file)
        file.seek(0)  # Torna all'inizio del file
        next(reader)  # Salta l'header se presente
        
        for i, row in enumerate(reader, 1):
            try:
                if not row:  # Salta righe vuote
                    continue
                    
                text = row[0].strip()
                if not text:  # Salta se il testo è vuoto
                    continue
                
                # Assegna un CAP casuale dalla lista
                cap = random.choice(TEST_CAPS)
                
                print(f"\n📝 Elaborazione riga {i}/{total_rows-1}:")
                print(f"Testo: {text[:100]}...")
                print(f"CAP assegnato: {cap}")
                
                # Classifica il problema
                classification = classifier.classify_issue(text, cap)
                
                # Salva nel database
                db_issue = models.Issue(
                    text=text,
                    cap=cap,
                    source='test_csv',
                    classification=classification
                )
                db.add(db_issue)
                db.commit()
                
                print(f"✅ Classificato come: {classification.get('category', 'N/A')} "
                      f"(Urgenza: {classification.get('urgency', 'N/A')})")
                success += 1
                
            except Exception as e:
                print(f"❌ Errore alla riga {i}: {str(e)}")
                errors += 1
                continue
    
    return success, errors

def main():
    if len(sys.argv) != 2:
        print("Uso: python populate_from_csv.py <path_to_csv>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"❌ File non trovato: {csv_path}")
        sys.exit(1)
    
    print("\n🚀 Avvio popolazione database da CSV...")
    
    try:
        db = next(get_db())
        success, errors = process_csv(csv_path, db)
        
        print("\n📊 Riepilogo:")
        print(f"✅ Segnalazioni elaborate con successo: {success}")
        print(f"❌ Errori: {errors}")
        
    except Exception as e:
        print(f"\n❌ Errore critico: {str(e)}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()