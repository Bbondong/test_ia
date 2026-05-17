import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# =========================
# CONFIG
# =========================
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# modèle plus stable (important)
HF_MODEL = "google/flan-t5-small"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

SYSTEM_PROMPT = """
Tu es un assistant fintech expert.
Tu donnes des conseils simples sur la finance, paiements et fintech.
Tu n'es pas un conseiller financier officiel.
Tu refuses toute demande illégale ou frauduleuse.
Réponds clairement et simplement.
"""

# =========================
# FRONT
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# API CHAT
# =========================
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = (data.get("message") if data else "").strip()

        if not message:
            return jsonify({"error": "Message vide"}), 400

        if not HF_API_TOKEN:
            return jsonify({"error": "Token API manquant"}), 500

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": f"{SYSTEM_PROMPT}\nUser: {message}\nAssistant:",
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7
            }
        }

        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=90
        )

        # =========================
        # DEBUG (important)
        # =========================
        try:
            data = response.json()
        except Exception:
            return jsonify({
                "error": "Réponse IA invalide (non JSON)",
                "raw": response.text
            }), 500

        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        # =========================
        # ERREURS API
        # =========================
        if response.status_code != 200:
            return jsonify({
                "error": "Erreur API externe",
                "details": data
            }), response.status_code

        if isinstance(data, dict) and data.get("error"):
            return jsonify({"error": data["error"]}), 500

        if not isinstance(data, list):
            return jsonify({
                "error": "Format IA invalide",
                "raw": data
            }), 500

        answer = data[0].get("generated_text", "")

        if "Assistant:" in answer:
            answer = answer.split("Assistant:")[-1].strip()

        return jsonify({"reply": answer})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)