import groq
import os
from dotenv import load_dotenv

load_dotenv()

class IssueClassifier:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-70b-versatile"
        
        # Categorie dettagliate per problemi della PA italiana
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
            
            # Eventi e Cultura
            "events": "Problemi relativi a eventi pubblici",
            "culture": "Strutture culturali (biblioteche, musei)",
            "sport": "Impianti sportivi pubblici",
            
            # Altro
            "animals": "Problemi con animali (randagi, infestazioni)",
            "emergency": "Situazioni di emergenza",
            "other": "Altri problemi non categorizzati"
        }

    def classify_issue(self, issue_text: str, cap: str) -> dict:
        categories_list = "\n".join([f"- {k}: {v}" for k, v in self.categories.items()])
        
        prompt = f"""Analizza il seguente problema relativo alla pubblica amministrazione italiana e classificalo.
        Il CAP fornito è: {cap}

        Categorie disponibili:
        {categories_list}

        Problema:
        {issue_text}

        Basandoti sul testo del problema e sul CAP, fornisci una risposta in formato JSON con:
        - category: la categoria specifica del problema (usa solo le chiavi delle categorie fornite)
        - confidence: livello di confidenza (0-1)
        - explanation: breve spiegazione della classificazione in italiano
        - urgency: livello di urgenza (low, medium, high)
        - zone_type: deduci il tipo di zona (residential, commercial, industrial, public_space) dal contesto e dal CAP
        - macro_category: deduci la categoria generale (infrastructure, environment, services, mobility, safety, utilities, culture)
        - area_details: analisi della zona basata sul CAP (es: "zona periferica", "centro storico", "area industriale", ecc.)
        - suggested_actions: suggerisci 2-3 azioni concrete per risolvere il problema
        """

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=self.model,
            temperature=0.1,
        )

        return chat_completion.choices[0].message.content

def test_groq_api():
    try:
        classifier = IssueClassifier()
        test_text = "C'è un albero caduto che blocca Via Roma dopo il temporale di ieri"
        test_cap = "20019"  # esempio: Settimo Milanese
        
        print("🔄 Testing Groq API...")
        result = classifier.classify_issue(test_text, test_cap)
        print("\n✅ Risposta ricevuta da Groq:")
        print(result)
        
    except Exception as e:
        print("❌ Errore durante il test dell'API Groq:")
        print(str(e))
