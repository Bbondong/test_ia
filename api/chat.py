import os
import requests
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔥 LOG CONFIG
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

MODEL_URL = "https://api-inference.huggingface.co/models/HuggingFaceTB/SmolLM-1.7B-Instruct"

SYSTEM_PROMPT = "Tu es un assistant fintech simple, clair et professionnel."

@app.route("/")
def home():
    logger.info("GET / called")
    return "API OK"

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        logger.info("=== NEW REQUEST /api/chat ===")

        # 🔍 check token
        if not HF_API_TOKEN:
            logger.error("HF_API_TOKEN missing")
            return jsonify({"error": "API token non configuré"}), 500

        data = request.get_json()
        logger.info(f"Request body: {data}")

        message = data.get("message", "")

        if not message:
            logger.warning("Empty message received")
            return jsonify({"error": "Message vide"}), 400

        logger.info(f"User message: {message}")

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

        logger.info("Sending request to Hugging Face API...")

        res = requests.post(MODEL_URL, headers=headers, json=payload, timeout=30)

        logger.info(f"HF status code: {res.status_code}")
        logger.info(f"HF raw response: {res.text}")

        data = res.json()

        # ❌ erreur API externe
        if isinstance(data, dict) and data.get("error"):
            logger.error(f"HF error: {data}")
            return jsonify({"error": data["error"]}), 500

        reply = data[0]["generated_text"].split("Assistant:")[-1].strip()

        logger.info(f"AI reply: {reply}")

        return jsonify({"reply": reply})

    except Exception as e:
        logger.exception("Unexpected error")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logger.info("Server starting...")
    app.run(host="0.0.0.0", port=5000)