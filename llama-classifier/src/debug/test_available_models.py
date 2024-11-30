import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import groq
from dotenv import load_dotenv

load_dotenv()

def test_available_models():
    try:
        client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        print("🔄 Recupero lista modelli disponibili...")
        models = client.models.list()
        
        print("\n✅ Modelli disponibili su Groq:")
        for model in models:
            print(f"\n- ID: {model.id}")
            if hasattr(model, 'owned_by'):
                print(f"  Owned by: {model.owned_by}")
            if hasattr(model, 'context_window'):
                print(f"  Context Window: {model.context_window} tokens")
            
    except Exception as e:
        print("❌ Errore durante il recupero dei modelli:")
        print(str(e))

if __name__ == "__main__":
    test_available_models() 