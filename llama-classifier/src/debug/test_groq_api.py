import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.services.classifier import IssueClassifier

def test_groq_api():
    try:
        classifier = IssueClassifier()
        test_text = "L'applicazione si blocca quando provo a salvare un file PDF"
        
        print("🔄 Testing Groq API...")
        result = classifier.classify_issue(test_text)
        print("\n✅ Risposta ricevuta da Groq:")
        print(result)
        
    except Exception as e:
        print("❌ Errore durante il test dell'API Groq:")
        print(str(e))

if __name__ == "__main__":
    test_groq_api() 