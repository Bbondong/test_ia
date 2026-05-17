import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)

# ======================
# CONFIG GROQ SAFE
# ======================
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("WARNING: GROQ_API_KEY manquante (configure Render env vars)")
    client = None
else:
    client = Groq(api_key=API_KEY)

# ======================
# SYSTEM PROMPT FINTECH STRICT
# ======================
SYSTEM_PROMPT = """
Tu es un assistant financier intelligent spécialisé uniquement dans la finance, la fintech, la gestion d'argent, les paiements, les banques, les investissements simples et l'éducation financière.

RÈGLES STRICTES :
- Tu refuses TOUT sujet qui n'est pas lié à la finance ou à la fintech.
- Si la question est hors sujet, réponds poliment :
  "Je suis un assistant financier et je peux uniquement aider sur des sujets liés à la finance et la gestion financière."

- Tu ne donnes jamais de conseils illégaux ou frauduleux.
- Tu restes clair, pédagogique et simple.

IDENTITÉ :
- Si on te demande qui t'a créé, tu réponds : "J'ai été créé par Bentech."

COMPORTEMENT :
- Toujours professionnel
- Toujours orienté finance
"""

# ======================
# FRONT
# ======================
@app.route("/")
def home():
    return render_template("index.html")


# ======================
# HEALTH CHECK
# ======================
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "groq_configured": client is not None
    })


# ======================
# CHAT API
# ======================
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        if client is None:
            return jsonify({
                "error": "Serveur non configuré (GROQ_API_KEY manquante)"
            }), 500

        data = request.get_json()
        message = (data.get("message") or "").strip()

        if not message:
            return jsonify({"error": "Message vide"}), 400

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.5,
            max_tokens=300
        )

        reply = completion.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Erreur serveur", "details": str(e)}), 500


# ======================
# RUN LOCAL
# ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)