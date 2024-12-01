import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.database.connection import DATABASE_URL
from src.database.models import Base

load_dotenv()

def init_database():
    try:
        # Crea l'engine
        engine = create_engine(DATABASE_URL)
        
        print("🔄 Inizializzazione del database...")
        
        # Crea il database se non esiste
        with engine.connect() as conn:
            conn.execute(text("commit"))
            
            # Crea le tabelle
            Base.metadata.create_all(engine)
            
            # Verifica le tabelle create
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            
            print("\n✅ Tabelle create con successo:")
            for row in result:
                print(f"- {row[0]}")
                
            # Verifica la struttura della tabella issues
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'issues'
            """))
            
            print("\nStruttura della tabella 'issues':")
            for row in result:
                print(f"- {row[0]}: {row[1]}")
                
    except Exception as e:
        print("❌ Errore durante l'inizializzazione del database:")
        print(str(e))

if __name__ == "__main__":
    init_database() 