import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.connection import engine
from sqlalchemy import text

def test_db_connection():
    try:
        # Testa la connessione
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Connessione al database riuscita!")
            
            # Mostra le tabelle esistenti
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            print("\nTabelle nel database:")
            for row in result:
                print(f"- {row[0]}")
                
    except Exception as e:
        print("❌ Errore di connessione al database:")
        print(str(e))

if __name__ == "__main__":
    test_db_connection() 