import json
import os
import hashlib

CACHE_DIR = "data/ai_cache"

def _get_path(country: str, question: str) -> str:
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    hash_key = hashlib.sha256(f"{country}_{question.lower().strip()}".encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{hash_key}.json")

def read_cache(country: str, question: str):
    path = _get_path(country, question)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def write_cache(country: str, question: str, answer: str):
    path = _get_path(country, question)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"answer": answer, "country": country, "question": question}, f)