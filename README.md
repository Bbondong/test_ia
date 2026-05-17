# 💰 FinTech AI - Analyse Financière Intelligente

Une application web complète pour l'analyse financière utilisant l'intelligence artificielle et les modèles gratuits de Hugging Face.

## 🎯 Fonctionnalités

### 📊 Analyse de Sentiment
- Analysez le sentiment des textes financiers et actualités
- Utilisez DistilBERT pour l'analyse générale
- Utilisez FinBERT pour l'analyse financière spécialisée
- Confiance de prédiction en pourcentage

### ⚠️ Analyse de Risque
- Calculez le score de risque d'un investissement
- Facteurs: volatilité, ratio d'endettement, liquidité
- Classification: BAS | MOYEN | ÉLEVÉ
- Visualisation circulaire en temps réel

### 📈 Prédiction de Tendance
- Prédisez la tendance basée sur les données historiques
- Graphique interactif des prix
- Calcul de la volatilité
- Direction de tendance: HAUSSIÈRE ou BAISSIÈRE

### 💼 Analyse de Portefeuille
- Ajoutez et gérez vos actifs
- Calcul de la répartition optimale
- Analyse du risque du portefeuille
- Visualisation de l'allocation

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Node.js (optionnel, pour le développement)
- pip

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone <url-du-repo>
cd fintech-ai
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration des variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et ajouter votre token Hugging Face (optionnel)
```

5. **Lancer l'application**
```bash
python api/chat.py
```

L'application sera accessible sur `http://localhost:5000`

## 🚀 Déploiement

### Déploiement sur Vercel

1. **Connecter votre repository GitHub**
```bash
git remote add origin <url>
git push -u origin main
```

2. **Configurer sur Vercel**
- Aller sur [vercel.com](https://vercel.com)
- Connecter votre GitHub
- Importer le projet
- Ajouter les variables d'environnement
- Déployer

### Déploiement sur Heroku

```bash
heroku create fintech-ai
git push heroku main
```

### Déploiement Docker

```bash
docker build -t fintech-ai .
docker run -p 5000:5000 fintech-ai
```

## 📚 API Endpoints

### `/api/health` - Vérifier l'état
```bash
GET /api/health
```

### `/api/analyze-sentiment` - Analyser le sentiment
```bash
POST /api/analyze-sentiment
{
    "text": "Apple a eu de excellents résultats cette année"
}
```

### `/api/analyze-financial` - Analyse financière avec FinBERT
```bash
POST /api/analyze-financial
{
    "text": "Risque élevé de récession économique"
}
```

### `/api/calculate-risk` - Calculer le risque
```bash
POST /api/calculate-risk
{
    "volatility": 15,
    "debt_ratio": 30,
    "liquidity": 1.5
}
```

### `/api/predict-trend` - Prédire la tendance
```bash
POST /api/predict-trend
{
    "historical_data": [100, 105, 103, 110, 115]
}
```

### `/api/portfolio-analysis` - Analyser un portefeuille
```bash
POST /api/portfolio-analysis
{
    "portfolio": [
        {"name": "Apple", "value": 5000, "risk": 0.6},
        {"name": "Gold", "value": 3000, "risk": 0.2}
    ]
}
```

## 🤖 Modèles IA Utilisés

1. **DistilBERT** (`distilbert-base-uncased-finetuned-sst-2-english`)
   - Analyse générale du sentiment
   - Modèle léger et rapide
   - Gratuit sur Hugging Face

2. **FinBERT** (`ProsusAI/finbert`)
   - Analyse spécialisée en finance
   - Entraîné sur des données financières
   - Gratuit et open-source

## 📊 Structure du Projet

```
fintech-ai/
├── api/
│   └── chat.py              # Backend Flask avec IA
├── public/
│   ├── index.html           # Interface web
│   ├── style.css            # Styles CSS
│   └── script.js            # Frontend JavaScript
├── requirements.txt         # Dépendances Python
├── vercel.json             # Configuration Vercel
├── .env.example            # Variables d'environnement
└── README.md               # Cette documentation
```

## 🔒 Sécurité

- Utilisation de variables d'environnement pour les secrets
- CORS activé pour contrôler l'accès
- Validation des entrées
- Gestion des erreurs robuste

## 📈 Améliorations Futures

- [ ] Authentification utilisateur
- [ ] Base de données pour historique
- [ ] Webhooks pour notifications
- [ ] Export de rapports PDF
- [ ] Intégration APIs financières externes
- [ ] Dashboard temps réel
- [ ] Machine Learning personnalisé
- [ ] Support multilingue

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir `LICENSE` pour plus de détails.

## 💬 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation
- Vérifier les discussions existantes

## 🙏 Remerciements

- [Hugging Face](https://huggingface.co) pour les modèles IA gratuits
- [Flask](https://flask.palletsprojects.com) pour le framework
- [Transformers](https://huggingface.co/docs/transformers) pour les outils NLP

## 📞 Contact

- Email: contact@fintech-ai.com
- GitHub: [@fintech-ai](https://github.com/fintech-ai)
- Twitter: [@FinTechAI](https://twitter.com/fintech-ai)

---

**Fait avec ❤️ et IA** | 2024
