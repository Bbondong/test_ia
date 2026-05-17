import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

HF_API_TOKEN = os.getenv('HF_API_TOKEN')
HF_MODEL = 'HuggingFaceTB/SmolLM-1.7B-Instruct'
HF_API_URL = f'https://api-inference.huggingface.co/models/{HF_MODEL}'

SYSTEM_PROMPT = (
    "Tu es un assistant fintech expert.\n"
    "Tu donnes des conseils généraux sur la finance, les paiements et la fintech.\n"
    "Tu n'es pas un conseiller financier officiel.\n"
    "Tu refuses toute demande illégale ou frauduleuse.\n"
    "Réponds de façon claire, simple et prudente.\n"
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()

        if not message:
            return jsonify({'error': 'Message requis'}), 400

        if not HF_API_TOKEN:
            return jsonify({'error': 'API token non configuré'}), 500

        headers = {
            'Authorization': f'Bearer {HF_API_TOKEN}',
            'Content-Type': 'application/json'
        }

        payload = {
            'inputs': f'{SYSTEM_PROMPT}\nUtilisateur: {message}\nAssistant:',
            'parameters': {
                'max_new_tokens': 300,
                'temperature': 0.7
            }
        }

        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=45
        )

        if response.status_code != 200:
            return jsonify({'error': 'Erreur API externe'}), response.status_code

        data = response.json()
        answer = data[0]['generated_text']
        answer = answer.split('Assistant:')[-1].strip()

        return jsonify({'reply': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)
