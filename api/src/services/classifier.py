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
        """Estrae il JSON dalla risposta del modello."""
        try:
            self._debug_log("Testo da parsare:", text)
            # Cerca il primo JSON valido nel testo
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                self._debug_log("JSON trovato:", json_str)
                return json.loads(json_str)
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
        try:
            # Step 1: Valutazione della validità della segnalazione
            validation_prompt = f"""Sei un esperto di segnalazioni della PA italiana.
            Valuta se questa segnalazione è valida e utile:
            "{issue_text}"
            
            Rispondi SOLO con un JSON:
            {{
                "is_valid": true/false,
                "reason": "spiegazione della decisione"
            }}
            
            Una segnalazione è valida se:
            - È una vera problematica della PA
            - Non è spam o contenuto offensivo
            - Non è un test o una prova
            - Ha un contenuto comprensibile e specifico
            - Richiede un'azione concreta
            """

            validation_response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Sei un validatore di segnalazioni della PA italiana."},
                    {"role": "user", "content": validation_prompt}
                ],
                model=self.model,
                temperature=0.3
            )

            validation_data = self._extract_json_from_text(validation_response.choices[0].message.content)
            self._debug_log("Risultato validazione:", validation_data)

            if not validation_data or not validation_data.get('is_valid', False):
                self._debug_log("Segnalazione non valida:", {
                    "text": issue_text,
                    "reason": validation_data.get('reason') if validation_data else "Errore nella validazione"
                })
                return {
                    "valid": False,
                    "reason": validation_data.get('reason', "Segnalazione non valida") if validation_data else "Errore nella validazione"
                }

            # Se la segnalazione è valida, procedi con la classificazione normale
            # Step 2: Geolocalizzazione dal CAP
            geo_prompt = f"""Sei un esperto di geografia italiana.
            Per il CAP {cap}, fornisci SOLO un JSON con:
            {{
                "city": "nome esatto della città",
                "coordinates": [latitudine, longitudine]
            }}
            IMPORTANTE: Devi essere preciso e accurato."""

            geo_response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Sei un esperto di geolocalizzazione italiana."},
                    {"role": "user", "content": geo_prompt}
                ],
                model=self.model,
                temperature=0.1
            )
            
            geo_data = self._extract_json_from_text(geo_response.choices[0].message.content)
            self._debug_log("Dati geografici ottenuti:", geo_data)

            # Step 3: Classificazione del problema
            categories_list = "\n".join([f"- {k}: {v}" for k, v in self.categories.items()])
            class_prompt = f"""Analizza questo problema della PA italiana:
            {issue_text}

            Categorie disponibili:
            {categories_list}

            Rispondi SOLO con un JSON:
            {{
                "category": "categoria del problema",
                "urgency": "livello di urgenza (low, medium, high)",
                "explanation": "descrivi il feedback con una frase da 2 a 5 parole"
            }}"""

            class_response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Sei un esperto di problemi della PA italiana."},
                    {"role": "user", "content": class_prompt}
                ],
                model=self.model,
                temperature=0.3
            )

            class_data = self._extract_json_from_text(class_response.choices[0].message.content)
            self._debug_log("Dati classificazione ottenuti:", class_data)

            # Combina i risultati solo se la segnalazione è valida
            if geo_data and class_data:
                final_result = {
                    "valid": True,
                    "original_text": issue_text,
                    "city": geo_data.get("city", "Unknown"),
                    "coordinates": geo_data.get("coordinates", [0, 0]),
                    "category": class_data.get("category", "other"),
                    "urgency": class_data.get("urgency", "medium"),
                    "explanation": class_data.get("explanation", "Nessuna spiegazione disponibile")
                }
                self._debug_log("Risultato finale combinato:", final_result)
                return final_result
            else:
                self._debug_log("Errore: dati mancanti", {
                    "geo_data": geo_data,
                    "class_data": class_data
                })
                return {
                    "valid": False,
                    "original_text": issue_text,
                    "reason": "Errore nell'elaborazione dei dati"
                }

        except Exception as e:
            self._debug_log(f"Errore durante la classificazione: {str(e)}")
            return {
                "valid": False,
                "original_text": issue_text,
                "reason": f"Errore tecnico: {str(e)}"
            }
