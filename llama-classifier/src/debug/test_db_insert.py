import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.connection import SessionLocal
from src.database.models import Issue

def test_db_insert():
    db = SessionLocal()
    try:
        # Crea un record di test
        test_issue = Issue(
            text="Test issue",
            classification={"category": "bug", "confidence": 0.9, "explanation": "Test"}
        )
        
        # Salva nel database
        db.add(test_issue)
        db.commit()
        print("✅ Record inserito con successo!")
        
        # Verifica l'inserimento
        issues = db.query(Issue).all()
        print("\nRecord nel database:")
        for issue in issues:
            print(f"- ID: {issue.id}")
            print(f"  Testo: {issue.text}")
            print(f"  Classificazione: {issue.classification}")
            print(f"  Creato il: {issue.created_at}")
            print()
            
    except Exception as e:
        print("❌ Errore durante l'inserimento:")
        print(str(e))
    finally:
        db.close()

if __name__ == "__main__":
    test_db_insert() 