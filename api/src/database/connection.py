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

# Stringa di connessione con parametri aggiuntivi
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configurazione del engine con parametri ottimizzati
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Funzione per ottenere una sessione del database"""
    db = SessionLocal()
    try:
        return db
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
        finally:
            db.close()
