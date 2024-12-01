from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import time
from contextlib import contextmanager

# Carica le variabili d'ambiente
load_dotenv()

# Configurazione del database
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Stringa di connessione con parametri aggiuntivi per la gestione delle disconnessioni
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configurazione del engine con parametri di connessione ottimizzati
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,  # Numero di connessioni nel pool
    max_overflow=10,  # Numero massimo di connessioni extra
    pool_timeout=30,  # Timeout per ottenere una connessione
    pool_recycle=1800,  # Ricicla connessioni dopo 30 minuti
    pool_pre_ping=True,  # Verifica la connessione prima dell'uso
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

def get_db_with_retry(max_retries=3, delay=1):
    """Funzione per ottenere una connessione al database con retry"""
    for attempt in range(max_retries):
        try:
            db = SessionLocal()
            db.execute("SELECT 1")  # Test della connessione
            return db
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
            continue
