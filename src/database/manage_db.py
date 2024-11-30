import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.database.connection import DATABASE_URL
from src.database.models import Base

load_dotenv()

def create_tables():
    """Crea tutte le tabelle nel database"""
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        print("✅ Tabelle create con successo!")
    except Exception as e:
        print("❌ Errore durante la creazione delle tabelle:")
        print(str(e))

def truncate_tables():
    """Svuota tutte le tabelle nel database"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Disabilita temporaneamente i vincoli di foreign key
            conn.execute(text("SET CONSTRAINTS ALL DEFERRED"))
            
            # Svuota la tabella issues
            conn.execute(text("TRUNCATE TABLE issues RESTART IDENTITY CASCADE"))
            
            conn.execute(text("commit"))
        print("✅ Tabelle svuotate con successo!")
    except Exception as e:
        print("❌ Errore durante lo svuotamento delle tabelle:")
        print(str(e))

def drop_tables():
    """Elimina tutte le tabelle"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Disabilita temporaneamente i vincoli di foreign key
            conn.execute(text("SET CONSTRAINTS ALL DEFERRED"))
            
            # Ottieni lista delle tabelle
            result = conn.execute(text("""
                SELECT tablename FROM pg_tables WHERE schemaname = 'public'
            """))
            
            # Elimina ogni tabella
            for row in result:
                table_name = row[0]
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
            
            conn.execute(text("commit"))
        print("✅ Tabelle eliminate con successo!")
    except Exception as e:
        print("❌ Errore durante l'eliminazione delle tabelle:")
        print(str(e))

def drop_and_create():
    """Elimina e ricrea tutte le tabelle"""
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.drop_all(engine)
        print("✅ Tabelle eliminate con successo!")
        Base.metadata.create_all(engine)
        print("✅ Tabelle ricreate con successo!")
    except Exception as e:
        print("❌ Errore durante l'eliminazione e ricreazione delle tabelle:")
        print(str(e))

def show_tables_info():
    """Mostra informazioni sulle tabelle esistenti"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Lista delle tabelle
            result = conn.execute(text("""
                SELECT table_name, 
                       (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as columns,
                       pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as size,
                       (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_name = t.table_name) as constraints
                FROM (
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                ) t;
            """))
            
            print("\nInformazioni sulle tabelle:")
            print("TABELLA | COLONNE | DIMENSIONE | VINCOLI")
            print("-" * 50)
            for row in result:
                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
                
    except Exception as e:
        print("❌ Errore durante il recupero delle informazioni:")
        print(str(e))

def main_menu():
    while True:
        print("\n🗄️  Gestione Database")
        print("-" * 30)
        print("1. Mostra informazioni tabelle")
        print("2. Crea tabelle")
        print("3. Svuota tabelle (mantiene struttura)")
        print("4. Elimina tabelle")
        print("5. Elimina e ricrea tabelle")
        print("0. Esci")
        
        choice = input("\nScegli un'opzione (0-5): ")
        
        if choice == "1":
            show_tables_info()
        elif choice == "2":
            create_tables()
        elif choice == "3":
            confirm = input("⚠️  Sei sicuro di voler svuotare tutte le tabelle? (s/n): ")
            if confirm.lower() == 's':
                truncate_tables()
        elif choice == "4":
            confirm = input("⚠️  Sei sicuro di voler eliminare tutte le tabelle? (s/n): ")
            if confirm.lower() == 's':
                drop_tables()
        elif choice == "5":
            confirm = input("⚠️  Sei sicuro di voler eliminare e ricreare tutte le tabelle? (s/n): ")
            if confirm.lower() == 's':
                drop_and_create()
        elif choice == "0":
            print("\n👋 Arrivederci!")
            break
        else:
            print("\n❌ Scelta non valida. Riprova.")
        
        input("\nPremi INVIO per continuare...")

if __name__ == "__main__":
    main_menu() 