import requests
import json
import os
import hashlib
import tempfile
import logging

logger = logging.getLogger(__name__)

# === GESTION DU CACHE AVEC DOSSIER TEMPORAIRE ===
CACHE_DIR = os.path.join(tempfile.gettempdir(), "ai_cache")
_CACHE_AVAILABLE = None

def _ensure_cache_dir():
    global _CACHE_AVAILABLE
    if _CACHE_AVAILABLE is not None:
        return _CACHE_AVAILABLE
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        # Test d'écriture
        test_file = os.path.join(CACHE_DIR, ".write_test")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        _CACHE_AVAILABLE = True
    except (OSError, IOError) as e:
        logger.warning(f"Cache non disponible : {e}")
        _CACHE_AVAILABLE = False
    return _CACHE_AVAILABLE

def _get_cache_path(country: str, question: str) -> str:
    hash_key = hashlib.sha256(f"{country}_{question.lower().strip()}".encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{hash_key}.json")

def read_cache(country: str, question: str):
    if not _ensure_cache_dir():
        return None
    try:
        path = _get_cache_path(country, question)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Erreur lecture cache : {e}")
    return None

def write_cache(country: str, question: str, answer: str):
    if not _ensure_cache_dir():
        return
    try:
        path = _get_cache_path(country, question)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"answer": answer, "country": country, "question": question}, f)
    except Exception as e:
        logger.warning(f"Erreur écriture cache : {e}")

# === PROMPT SYSTÈME ===
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