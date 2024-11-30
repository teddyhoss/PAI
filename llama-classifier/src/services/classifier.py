import groq
import os
from dotenv import load_dotenv

load_dotenv()

class IssueClassifier:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama2-70b-4096"  # o il modello che preferisci

    async def classify_issue(self, issue_text: str) -> dict:
        prompt = f"""Analizza il seguente problema e classificalo in una delle seguenti categorie:
        - bug
        - feature_request
        - documentation
        - security
        - performance
        - other

        Problema:
        {issue_text}

        Fornisci una risposta in formato JSON con:
        - category: la categoria del problema
        - confidence: livello di confidenza (0-1)
        - explanation: breve spiegazione della classificazione
        """

        chat_completion = await self.client.chat.completions.create(
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
