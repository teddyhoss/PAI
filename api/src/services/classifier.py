import groq
import os
import json
import re
from dotenv import load_dotenv
from typing import Dict, Any
import logging
from datetime import datetime

load_dotenv()

# Configurazione del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('classifier')

class IssueClassifier:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-70b-versatile"
        self.max_retries = 3
        self.debug = os.getenv("CLASSIFIER_DEBUG", "false").lower() == "true"
        
        # Categorie per problemi della PA italiana
        self.categories = {
            # Infrastrutture e Manutenzione
            "roads": "Strade, buche, segnaletica stradale",
            "lighting": "Illuminazione pubblica",
            "buildings": "Edifici pubblici, scuole, uffici comunali",
            "sidewalks": "Marciapiedi e aree pedonali",
            
            # Ambiente e Verde
            "garbage": "Rifiuti e pulizia stradale",
            "parks": "Parchi, giardini pubblici",
            "trees": "Alberi e verde urbano",
            "pollution": "Inquinamento (aria, acqua, rumore)",
            
            # Servizi Pubblici
            "bureaucracy": "Problemi burocratici e amministrativi",
            "health": "Servizi sanitari locali",
            "education": "Servizi scolastici e educativi",
            "social": "Servizi sociali e assistenza",
            
            # Mobilità
            "public_transport": "Trasporto pubblico (bus, metro)",
            "parking": "Parcheggi e sosta",
            "traffic": "Traffico e viabilità",
            "cycling": "Piste ciclabili",
            
            # Sicurezza e Ordine
            "public_safety": "Sicurezza pubblica",
            "vandalism": "Vandalismo e degrado",
            "noise": "Disturbo della quiete pubblica",
            
            # Utilities
            "water": "Acquedotto e problemi idrici",
            "electricity": "Rete elettrica pubblica",
            "internet": "Connettività e servizi digitali pubblici",
            
            # Altro
            "emergency": "Situazioni di emergenza",
            "other": "Altri problemi non categorizzati"
        }
        
        # Configurazione logger migliorata
        if self.debug:
            os.makedirs('logs', exist_ok=True)
            log_file = f'logs/classifier_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.setLevel(logging.DEBUG)
            logger.debug(f"Inizializzazione classifier - Log file: {log_file}")

    def _debug_log(self, message: str, data: Any = None):
        """Funzione helper per logging in modalità debug"""
        if self.debug:
            if data:
                logger.debug(f"{message}: {json.dumps(data, indent=2, ensure_ascii=False)}")
            else:
                logger.debug(message)

    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """Estrae il JSON dalla risposta del modello usando regex."""
        try:
            # Log del testo completo ricevuto
            self._debug_log("Testo completo ricevuto per estrazione JSON:", text)
            
            # Pattern regex migliorato per catturare JSON più complessi
            json_pattern = r'\{(?:[^{}]|(?R))*\}'
            json_matches = re.finditer(json_pattern, text, re.DOTALL)
            
            for match in json_matches:
                try:
                    json_str = match.group(0)
                    self._debug_log("Tentativo di parsing JSON:", json_str)
                    json_obj = json.loads(json_str)
                    
                    # Verifica che il JSON contenga i campi richiesti
                    required_fields = ['category', 'urgency', 'explanation', 'city', 'coordinates']
                    if all(field in json_obj for field in required_fields):
                        self._debug_log("JSON valido trovato:", json_obj)
                        return json_obj
                except json.JSONDecodeError as e:
                    self._debug_log(f"Errore nel parsing JSON: {str(e)}")
                    continue
            
            self._debug_log("Nessun JSON valido trovato nel testo")
            return None
            
        except Exception as e:
            self._debug_log(f"Errore nell'estrazione JSON: {str(e)}")
            return None

    def _validate_response(self, response: Dict[str, Any]) -> bool:
        """Verifica che la risposta contenga tutti i campi necessari."""
        required_fields = ['category', 'urgency', 'explanation', 'city', 'coordinates']
        return all(field in response for field in required_fields)

    def _format_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Formatta e standardizza la risposta."""
        return {
            'category': str(response.get('category', 'other')),
            'urgency': str(response.get('urgency', 'medium')).lower(),
            'explanation': str(response.get('explanation', 'Nessuna spiegazione disponibile')),
            'city': str(response.get('city', 'Unknown')),
            'coordinates': response.get('coordinates', [0, 0])
        }

    def classify_issue(self, issue_text: str, cap: str) -> dict:
        for attempt in range(self.max_retries):
            try:
                categories_list = "\n".join([f"- {k}: {v}" for k, v in self.categories.items()])
                
                prompt = f"""Sei un assistente specializzato nell'analisi di problemi della pubblica amministrazione italiana.
                La tua priorità è determinare con precisione la città e le coordinate geografiche dal CAP fornito.
                
                CAP: {cap}
                
                1. Prima determina la città corrispondente al CAP
                2. Trova le coordinate geografiche precise della città
                3. Poi analizza il seguente problema:
                {issue_text}

                Categorie disponibili:
                {categories_list}

                IMPORTANTE: Rispondi SOLO con un JSON valido che DEVE contenere questi campi:
                {{
                    "category": "categoria del problema (una tra quelle elencate)",
                    "urgency": "livello di urgenza (low, medium, high)",
                    "explanation": "breve spiegazione in italiano della classificazione",
                    "city": "nome esatto della città",
                    "coordinates": [latitudine, longitudine]
                }}
                """

                self._debug_log("Invio prompt al modello", {"cap": cap, "issue_text": issue_text})
                
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model,
                    temperature=0.3,
                )

                response_text = response.choices[0].message.content
                self._debug_log("Risposta ricevuta dal modello", {"response": response_text})

                json_response = self._extract_json_from_text(response_text)
                if json_response:
                    self._debug_log("JSON estratto", json_response)
                    if self._validate_response(json_response):
                        formatted_response = self._format_response(json_response)
                        self._debug_log("Risposta finale formattata", formatted_response)
                        return formatted_response
                    else:
                        self._debug_log("Validazione fallita - campi mancanti", json_response)
                else:
                    self._debug_log("Estrazione JSON fallita")

                if attempt == self.max_retries - 1:
                    self._debug_log("Tutti i tentativi falliti, ritorno risposta di default")
                    return self._format_response({})

            except Exception as e:
                self._debug_log(f"Errore durante l'esecuzione: {str(e)}")
                if attempt == self.max_retries - 1:
                    return self._format_response({})
                continue

        return self._format_response({})
