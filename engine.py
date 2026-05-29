import requests
from cache_manager import read_cache, write_cache
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Tu es Arnold, l'expert Fintech senior de JTM KING PAY. 
TON APPROCHE: Avant chaque réponse, analyse la demande de l'utilisateur. 
TON STYLE: Formel, expert, structuré et didactique.

STRUCTURE DE RÉPONSE OBLIGATOIRE:
1. Analyse: Une phrase d'analyse sur le besoin exprimé.
2. Stratégie: Développement du conseil principal (ex: la règle 50/30/20).
3. Action: Une recommandation spécifique sur comment utiliser JTM KING PAY pour optimiser cela.
4. Sécurité: Un rappel bref sur la protection des accès.

RÈGLES:
- Pas de blabla inutile. Chaque phrase doit apporter de la valeur.
- Ton expert: Analyser les tendances du marché selon le code pays (+243).
- Fallback: Si la demande est hors champ ou sensible: "Je m'excuse, mais ma zone d'expertise actuelle ne me permet pas de répondre à cette demande précise. Je vous redirige vers un conseiller humain de JTM KING PAY pour vous assister."
"""

def generate_ai_response(question: str, country_code: str):
    cached = read_cache(country_code, question)
    if cached:
        return {"answer": cached["answer"], "source": "cache", "agent": "Arnold"}

    try:
        # On demande explicitement une structure détaillée mais dense
        instruction = "\nRéponds de manière développée en suivant strictement la structure (Analyse, Stratégie, Action, Sécurité)."
        full_prompt = f"{SYSTEM_PROMPT}{instruction}\nUser location: {country_code}\nQuestion: {question}"
        
        url = "https://cerveau-lysia.vercel.app/api/gpt"
        params = {"q": full_prompt}
        
        response = requests.get(url, params=params, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("message", "Je m'excuse, mais ma zone d'expertise actuelle ne me permet pas de répondre à cette demande précise.")
        else:
            raise Exception("API Lysia Error")

    except Exception:
        answer = "Je m'excuse, mais ma zone d'expertise actuelle ne me permet pas de répondre à cette demande précise. Je vous redirige vers un conseiller humain de JTM KING PAY pour vous assister."

    write_cache(country_code, question, answer)
    return {"answer": answer, "source": "llm", "agent": "Arnold"}