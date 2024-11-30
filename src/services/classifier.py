import groq
import os
from dotenv import load_dotenv

load_dotenv()

class IssueClassifier:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-70b-versatile"

    def classify_issue(self, issue_text: str) -> dict:
        prompt = f"""Analizza il seguente problema e classificalo in una delle seguenti categorie:
        - bug: problemi tecnici o malfunzionamenti
        - feature_request: richieste di nuove funzionalità
        - documentation: problemi o richieste relative alla documentazione
        - security: problemi di sicurezza
        - performance: problemi di prestazioni
        - other: altri tipi di problemi

        Problema:
        {issue_text}

        Fornisci una risposta in formato JSON con:
        - category: la categoria del problema
        - confidence: livello di confidenza (0-1)
        - explanation: spiegazione dettagliata della classificazione
        - severity: livello di gravità (low, medium, high)
        - suggested_priority: priorità suggerita (1-5)
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
