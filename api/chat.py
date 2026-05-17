from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import json
from transformers import pipeline
import numpy as np

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
HF_API_TOKEN = os.getenv('TOKEN') 
HF_MODEL_SENTIMENT = "distilbert-base-uncased-finetuned-sst-2-english"
HF_MODEL_FINANCIAL = "ProsusAI/finbert"

# Initialiser les pipelines
try:
    sentiment_pipeline = pipeline("sentiment-analysis", model=HF_MODEL_SENTIMENT)
    financial_pipeline = pipeline("text-classification", model=HF_MODEL_FINANCIAL)
except Exception as e:
    print(f"Erreur lors du chargement des modèles: {e}")
    sentiment_pipeline = None
    financial_pipeline = None

class FinanceAnalyzer:
    """Analyseur financier utilisant Hugging Face"""
    
    @staticmethod
    def analyze_sentiment(text):
        """Analyser le sentiment d'un texte financier"""
        try:
            if sentiment_pipeline:
                result = sentiment_pipeline(text[:512])[0]
                return {
                    'sentiment': result['label'],
                    'score': float(result['score']),
                    'success': True
                }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    @staticmethod
    def analyze_financial_text(text):
        """Analyser un texte avec le modèle FinBERT"""
        try:
            if financial_pipeline:
                result = financial_pipeline(text[:512])[0]
                return {
                    'label': result['label'],
                    'score': float(result['score']),
                    'success': True
                }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    @staticmethod
    def calculate_risk_score(data):
        """Calculer un score de risque basé sur les données"""
        try:
            volatility = data.get('volatility', 0)
            debt_ratio = data.get('debt_ratio', 0)
            liquidity = data.get('liquidity', 1)
            
            # Formule simple de calcul de risque
            risk_score = (volatility * 0.4 + debt_ratio * 0.4) / max(liquidity, 0.1)
            risk_score = min(100, max(0, risk_score * 10))
            
            return {
                'risk_score': float(risk_score),
                'risk_level': 'ÉLEVÉ' if risk_score > 70 else 'MOYEN' if risk_score > 40 else 'BAS',
                'success': True
            }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    @staticmethod
    def predict_trend(historical_data):
        """Prédire la tendance basée sur les données historiques"""
        try:
            if len(historical_data) < 2:
                return {'error': 'Données insuffisantes', 'success': False}
            
            prices = np.array(historical_data)
            trend = (prices[-1] - prices[0]) / prices[0] * 100
            
            # Calculer la volatilité
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns) * 100
            
            return {
                'trend_percent': float(trend),
                'volatility': float(volatility),
                'direction': '📈 HAUSSIÈRE' if trend > 0 else '📉 BAISSIÈRE',
                'success': True
            }
        except Exception as e:
            return {'error': str(e), 'success': False}

# Routes API
@app.route('/api/health', methods=['GET'])
def health():
    """Vérifier l'état de l'API"""
    return jsonify({
        'status': 'OK',
        'message': 'API FinTech est opérationnelle',
        'models_loaded': {
            'sentiment': sentiment_pipeline is not None,
            'financial': financial_pipeline is not None
        }
    })

@app.route('/api/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyser le sentiment d'un texte"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Texte requis'}), 400
        
        result = FinanceAnalyzer.analyze_sentiment(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/analyze-financial', methods=['POST'])
def analyze_financial():
    """Analyser un texte financier"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Texte requis'}), 400
        
        result = FinanceAnalyzer.analyze_financial_text(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/calculate-risk', methods=['POST'])
def calculate_risk():
    """Calculer le score de risque"""
    try:
        data = request.get_json()
        result = FinanceAnalyzer.calculate_risk_score(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/predict-trend', methods=['POST'])
def predict_trend():
    """Prédire la tendance"""
    try:
        data = request.get_json()
        historical_data = data.get('historical_data', [])
        
        if not historical_data:
            return jsonify({'error': 'Données historiques requises'}), 400
        
        result = FinanceAnalyzer.predict_trend(historical_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint de chat principal pour les requêtes financières"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        action = data.get('action', 'sentiment')
        
        if not user_message:
            return jsonify({'error': 'Message requis'}), 400
        
        if action == 'sentiment':
            result = FinanceAnalyzer.analyze_sentiment(user_message)
        elif action == 'financial':
            result = FinanceAnalyzer.analyze_financial_text(user_message)
        else:
            result = {'error': 'Action non reconnue', 'success': False}
        
        return jsonify({
            'user_message': user_message,
            'action': action,
            'analysis': result
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/portfolio-analysis', methods=['POST'])
def portfolio_analysis():
    """Analyser un portefeuille"""
    try:
        data = request.get_json()
        portfolio = data.get('portfolio', [])
        
        if not portfolio:
            return jsonify({'error': 'Portefeuille requis'}), 400
        
        total_value = sum(asset.get('value', 0) for asset in portfolio)
        total_risk = sum(asset.get('risk', 0) * asset.get('value', 0) for asset in portfolio) / total_value if total_value > 0 else 0
        
        allocation = [
            {
                'name': asset.get('name'),
                'percentage': (asset.get('value', 0) / total_value * 100) if total_value > 0 else 0,
                'value': asset.get('value', 0),
                'risk': asset.get('risk', 0)
            }
            for asset in portfolio
        ]
        
        return jsonify({
            'total_value': total_value,
            'average_risk': float(total_risk),
            'allocation': allocation,
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
