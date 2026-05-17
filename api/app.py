import os
import json
import requests

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

HF_MODEL = "HuggingFaceTB/SmolLM-1.7B-Instruct"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

SYSTEM_PROMPT = (
    "Tu es un assistant fintech.\n"
    "Tu donnes des conseils simples sur la finance, paiements et fintech.\n"
    "Tu refuses toute demande illégale.\n"
)

def handler(request):
    try:
        body = json.loads(request.body or "{}")
        message = body.get("message", "")

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": f"{SYSTEM_PROMPT}\nUser: {message}\nAssistant:",
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.4
            }
        }

        res = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=40
        )

        data = res.json()

        text = data[0]["generated_text"]
        text = text.split("Assistant:")[-1].strip()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"reply": text})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }