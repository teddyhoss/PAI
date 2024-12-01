import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.services.classifier import IssueClassifier

def test_groq():
    try:
        classifier = IssueClassifier()
        test_text = "C'è un albero caduto che blocca Via Roma"
        test_cap = "00100"
        
        print("🔄 Testing LLM con Groq API...")
        result = classifier.classify_issue(test_text, test_cap)
        print("\n✅ Test riuscito! Risposta del modello:")
        print(result)
        
    except Exception as e:
        print("❌ Errore di connessione a Groq:")
        print(str(e))

if __name__ == "__main__":
    test_groq() 