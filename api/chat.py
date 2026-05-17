import os
import json
import requests

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")
HF_MODEL = "HuggingFaceTB/SmolLM-1.7B-Instruct"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

SYSTEM_PROMPT = (
    "Tu es un assistant fintech expert.\n"
    "Tu donnes des conseils généraux sur la finance, les paiements et la fintech.\n"
    "Tu n'es pas un conseiller financier officiel.\n"
    "Tu refuses toute demande illégale ou frauduleuse.\n"
    "Réponds de façon claire, simple et prudente.\n"
    "Utilise des emojis pertinents pour rendre la réponse plus engageante.\n"
)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json"
}

def handler(request):
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": ""
        }
    
    try:
        body = json.loads(request.body or "{}")
        message = body.get("message", "").strip()

        if not message:
            return {
                "statusCode": 400,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Message requis"})
            }

        if not HF_API_TOKEN:
            return {
                "statusCode": 500,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "API token non configuré"})
            }

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": f"{SYSTEM_PROMPT}\nUtilisateur: {message}\nAssistant:",
            "parameters": {
                "max_new_tokens": 300,
                "temperature": 0.7
            }
        }

        res = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=45
        )

        if res.status_code != 200:
            return {
                "statusCode": res.status_code,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Erreur API externe"})
            }

        data = res.json()
        answer = data[0]["generated_text"]
        answer = answer.split("Assistant:")[-1].strip()

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({"reply": answer})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)})
        }