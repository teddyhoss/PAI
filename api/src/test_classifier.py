import requests
import json
import logging
from datetime import datetime
import os

# Configurazione logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('test_classifier')

# Configurazione file di log
os.makedirs('logs', exist_ok=True)
log_file = f'logs/test_classifier_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def test_classifier():
    # URL dell'API
    url = "http://localhost:8000/api/classify/"
    
    # Dati di test
    test_cases = [
        {
            "text": "C'è una buca pericolosa in via Roma che sta causando problemi al traffico",
            "cap": "40121"  # Bologna centro
        },
        {
            "text": "Il parco giochi è in stato di abbandono, con giochi rotti e sporcizia",
            "cap": "20121"  # Milano centro
        },
        {
            "text": "Mancanza di illuminazione pubblica in via Garibaldi",
            "cap": "00185"  # Roma
        }
    ]
    
    # Test ogni caso
    for i, test_case in enumerate(test_cases, 1):
        try:
            logger.info(f"\n=== Test Case {i} ===")
            logger.info(f"Invio richiesta con dati: {json.dumps(test_case, indent=2, ensure_ascii=False)}")
            
            # Invio richiesta POST
            response = requests.post(url, json=test_case)
            
            # Log della risposta
            logger.info(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info("Risposta ricevuta:")
                logger.info(json.dumps(result, indent=2, ensure_ascii=False))
                
                # Verifica dei campi principali
                logger.info("\nVerifica campi:")
                fields_to_check = ['city', 'coordinates', 'category', 'urgency', 'explanation']
                for field in fields_to_check:
                    if field in result.get('classification', {}):
                        logger.info(f"✓ {field}: {result['classification'][field]}")
                    else:
                        logger.warning(f"✗ Campo mancante: {field}")
            else:
                logger.error(f"Errore nella richiesta: {response.text}")
                
        except Exception as e:
            logger.error(f"Errore durante il test: {str(e)}")
        
        logger.info("\n" + "="*50 + "\n")

if __name__ == "__main__":
    logger.info("Inizio test del classifier")
    test_classifier()
    logger.info("Fine test del classifier") 