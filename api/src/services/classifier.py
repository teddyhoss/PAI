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
        
        if self.debug:
            os.makedirs('logs', exist_ok=True)
            fh = logging.FileHandler(f'logs/classifier_{datetime.now().strftime("%Y%m%d")}.log')
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.setLevel(logging.DEBUG)
            logger.debug("Modalità debug attivata per il classifier")

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
            json_match = re.search(r'\{[^{}]*\}', text)
            if json_match:
                return json.loads(json_match.group(0))
            return None
        except json.JSONDecodeError:
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
                
                prompt = f"""Analizza attentamente il seguente problema della pubblica amministrazione italiana.
                Prendi il tempo necessario per una valutazione accurata.
                
                Per il CAP {cap}, determina prima la città corrispondente e le sue coordinate geografiche.
                Poi analizza il problema fornito.
                
                CAP: {cap}
                Problema: {issue_text}

                Categorie disponibili:
                {categories_list}

                Rispondi SOLO con un JSON valido che contiene:
                {{
                    "category": "categoria del problema (una tra quelle elencate)",
                    "urgency": "livello di urgenza (low, medium, high)",
                    "explanation": "breve sintesi del feedback (2-10 parole massimo)",
                    "city": "nome della città",
                    "coordinates": [latitudine, longitudine]
                }}
                """

                self._debug_log(f"Tentativo {attempt + 1}/{self.max_retries}")
                self._debug_log("Prompt inviato", {"issue_text": issue_text, "cap": cap})

                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model,
                    temperature=0.3,  # Aumentato per dare più tempo di "pensare"
                )

                response_text = response.choices[0].message.content
                self._debug_log("Risposta ricevuta dal modello", {"response": response_text})

                json_response = self._extract_json_from_text(response_text)
                if json_response:
                    self._debug_log("JSON estratto con regex", json_response)
                else:
                    self._debug_log("Tentativo di estrazione JSON con regex fallito, provo parsing diretto")
                    try:
                        json_response = json.loads(response_text)
                        self._debug_log("JSON estratto con parsing diretto", json_response)
                    except json.JSONDecodeError as e:
                        self._debug_log(f"Errore nel parsing JSON: {str(e)}")
                        if attempt == self.max_retries - 1:
                            self._debug_log("Tutti i tentativi falliti, ritorno risposta di default")
                            return self._format_response({})
                        continue

                if self._validate_response(json_response):
                    formatted_response = self._format_response(json_response)
                    self._debug_log("Risposta validata e formattata con successo", formatted_response)
                    return formatted_response
                
                self._debug_log("Validazione risposta fallita")
                if attempt == self.max_retries - 1:
                    self._debug_log("Tutti i tentativi falliti, ritorno risposta di default")
                    return self._format_response({})

            except Exception as e:
                self._debug_log(f"Errore durante l'esecuzione: {str(e)}")
                if attempt == self.max_retries - 1:
                    self._debug_log("Tutti i tentativi falliti per errore, ritorno risposta di default")
                    return self._format_response({})
                continue

        return self._format_response({})
