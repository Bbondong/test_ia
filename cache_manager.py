import json
import os
import hashlib
import tempfile
import logging

# Utiliser un répertoire accessible en écriture (dossier temporaire)
CACHE_DIR = os.path.join(tempfile.gettempdir(), "ai_cache")
logger = logging.getLogger(__name__)

def _ensure_cache_dir():
    """Crée le répertoire de cache si nécessaire et vérifie les droits."""
    try:
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR, exist_ok=True)
        # Test d'écriture : créer un fichier test
        test_file = os.path.join(CACHE_DIR, ".write_test")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        return True
    except (OSError, IOError) as e:
        logger.warning(f"Impossible d'utiliser le cache ({CACHE_DIR}) : {e}")
        return False

# Variable globale pour savoir si le cache est utilisable
_CACHE_AVAILABLE = None

def _is_cache_available():
    global _CACHE_AVAILABLE
    if _CACHE_AVAILABLE is None:
        _CACHE_AVAILABLE = _ensure_cache_dir()
    return _CACHE_AVAILABLE

def _get_path(country: str, question: str) -> str:
    """Génère le chemin du fichier de cache."""
    hash_key = hashlib.sha256(f"{country}_{question.lower().strip()}".encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{hash_key}.json")

def read_cache(country: str, question: str):
    """Lit le cache si disponible."""
    if not _is_cache_available():
        return None
    try:
        path = _get_path(country, question)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Erreur lecture cache : {e}")
    return None

def write_cache(country: str, question: str, answer: str):
    """Écrit dans le cache si possible."""
    if not _is_cache_available():
        return
    try:
        path = _get_path(country, question)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"answer": answer, "country": country, "question": question}, f)
    except Exception as e:
        logger.warning(f"Erreur écriture cache : {e}")