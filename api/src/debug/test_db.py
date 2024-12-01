import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.connection import SessionLocal
from src.database.models import Issue

def test_db():
    try:
        db = SessionLocal()
        print("🔄 Testing connessione al database...")
        
        # Prova a fare una query
        count = db.query(Issue).count()
        print("✅ Connessione al database riuscita!")
        print(f"Numero di segnalazioni nel database: {count}")
            
    except Exception as e:
        print("❌ Errore di connessione al database:")
        print(str(e))
    finally:
        db.close()

if __name__ == "__main__":
    test_db() 