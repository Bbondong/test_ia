from flask import Flask, request, jsonify
from engine import generate_ai_response
import logging
import sys

# Configuration des logs pour tracer l'activité dans la console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = Flask(__name__)

# Route sécurisée pour interroger Arnold
@app.route("/ask", methods=["POST"])
def ask_arnold():
    # 1. Validation de l'en-tête (Content-Type)
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    # 2. Récupération des données
    data = request.get_json()
    if not data:
        return jsonify({"error": "Payload invalide, JSON requis"}), 400
    
    question = data.get("question")
    indicatif = data.get("indicatif", "Global")
    
    # 3. Validation des champs obligatoires
    if not question or len(question.strip()) == 0:
        return jsonify({"error": "La question est obligatoire"}), 400
    
    try:
        # Journalisation de l'activité
        logging.info(f"Requête reçue de [{indicatif}] : {question[:50]}...")
        
        # Appel du moteur IA (Arnold)
        response = generate_ai_response(question, indicatif)
        
        return jsonify(response), 200
        
    except Exception as e:
        # Journalisation de l'erreur côté serveur pour debug
        logging.error(f"Erreur interne lors du traitement : {str(e)}")
        
        # Réponse propre pour l'utilisateur mobile
        return jsonify({
            "answer": "Je m'excuse, mais ma zone d'expertise actuelle ne me permet pas de répondre à cette demande précise. Je vous redirige vers un conseiller humain de JTM KING PAY pour vous assister.",
            "source": "fallback",
            "agent": "Arnold"
        }), 500

if __name__ == "__main__":
    # Host 0.0.0.0 pour acceptation des connexions externes
    # Port 5001 pour éviter les conflits avec des services standards
    app.run(host="0.0.0.0", port=5003, debug=False)