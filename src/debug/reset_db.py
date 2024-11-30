import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.connection import engine, Base, SessionLocal
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

def reset_db():
    db = None
    try:
        # Verifica configurazione database
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        
        if not all([db_user, db_password, db_host, db_port, db_name]):
            print("❌ Mancano alcune variabili di configurazione del database nel file .env")
            return False
            
        db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        print(f"🔍 Database configurato: {db_host}:{db_port}/{db_name}")
        
        # Creo una sessione per gestire le connessioni attive
        db = SessionLocal()
        
        # Verifica connessione
        print("🔄 Verifico connessione al database...")
        result = db.execute(text("SELECT current_database()")).scalar()
        print(f"✅ Connesso al database: {result}")
        
        print("🔄 Chiudo tutte le connessioni attive...")
        db.execute(text("""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = current_database()
            AND pid <> pg_backend_pid()
        """))
        db.commit()
        
        print("🔄 Eliminazione di tutte le tabelle in corso...")
        
        # Ottieni lista di tutte le tabelle
        tables = db.execute(text("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """))
        
        # Disabilita temporaneamente i vincoli di chiave esterna
        db.execute(text("SET session_replication_role = 'replica';"))
        
        # Elimina ogni tabella
        for table in tables:
            table_name = table[0]
            print(f"Eliminazione tabella: {table_name}")
            db.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))
        
        # Riabilita i vincoli di chiave esterna
        db.execute(text("SET session_replication_role = 'origin';"))
        
        db.commit()
        print("✅ Database svuotato con successo!")
        
        # Verifica che non ci siano più tabelle
        remaining_tables = db.execute(text("""
            SELECT COUNT(*) 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """)).scalar()
        
        if remaining_tables == 0:
            print("✅ Tutte le tabelle sono state eliminate!")
        else:
            print(f"⚠️ Attenzione: {remaining_tables} tabelle ancora presenti")
        
        return True
        
    except Exception as e:
        print("\n❌ Errore durante l'eliminazione delle tabelle:")
        print(f"Errore: {str(e)}")
        return False
    finally:
        if db is not None:
            db.close()
            engine.dispose()

if __name__ == "__main__":
    print("🚀 Inizio pulizia database...")
    success = reset_db()
    if success:
        print("\n✅ Database ora è vuoto!")
    else:
        print("\n❌ Operazione fallita") 