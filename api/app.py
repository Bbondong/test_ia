import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

HF_MODEL = "HuggingFaceTB/SmolLM-1.7B-Instruct"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

SYSTEM_PROMPT = """
Tu es un assistant fintech.
Tu donnes des conseils simples sur la finance et les paiements.
Tu refuses les demandes illégales.
"""

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

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

    res = requests.post(HF_API_URL, headers=headers, json=payload, timeout=40)
    result = res.json()

    text = result[0]["generated_text"]
    text = text.split("Assistant:")[-1].strip()

    return jsonify({"reply": text})


# REQUIRED for Vercel detection
application = app