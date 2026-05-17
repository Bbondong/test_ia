import os
import json
import requests

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

HF_MODEL = "HuggingFaceTB/SmolLM-1.7B-Instruct"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

SYSTEM_PROMPT = (
    "Tu es un assistant fintech.\n"
    "Tu donnes des conseils généraux sur la finance, les paiements et la fintech.\n"
    "Tu n'es pas un conseiller financier officiel.\n"
    "Tu refuses toute demande illégale ou frauduleuse.\n"
    "Réponds de façon claire, simple et prudente.\n"
)

def handler(request):
    try:
        body = json.loads(request.body or "{}")
        message = body.get("message", "").strip()

        if not message:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Message vide"})
            }

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": f"{SYSTEM_PROMPT}\nUtilisateur: {message}\nAssistant:",
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.4
            }
        }

        res = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=45
        )

        data = res.json()
        answer = data[0]["generated_text"]
        answer = answer.split("Assistant:")[-1].strip()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"reply": answer})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }