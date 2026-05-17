import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

MODEL_URL = "https://api-inference.huggingface.co/models/HuggingFaceTB/SmolLM-1.7B-Instruct"

SYSTEM_PROMPT = "Tu es un assistant fintech simple, clair et professionnel."

@app.route("/")
def home():
    return "API OK"

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "Message vide"}), 400

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": f"{SYSTEM_PROMPT}\nUser: {message}\nAssistant:",
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.5
            }
        }

        res = requests.post(MODEL_URL, headers=headers, json=payload, timeout=30)
        data = res.json()

        # protection erreur API
        if isinstance(data, dict) and data.get("error"):
            return jsonify({"error": data["error"]}), 500

        reply = data[0]["generated_text"].split("Assistant:")[-1].strip()

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)