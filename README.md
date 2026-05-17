# FinTech AI Assistant | Architecture Vercel Production-Ready

## 📋 Structure du projet

```
.
├── api/
│   └── chat.py              # Serverless handler Python Vercel
├── public/
│   ├── index.html           # Frontend SPA
│   ├── style.css            # Styles modern
│   └── script.js            # Logique client
├── vercel.json              # Configuration Vercel
├── requirements.txt         # Dépendances Python
├── .env.example             # Variables d'environnement
└── README.md                # Ce fichier
```

## 🚀 Quick Start

### 1. Configuration locale

```bash
# Copier les variables d'environnement
cp .env.example .env

# Éditer .env avec votre token HF
# HF_API_TOKEN=hf_YOUR_TOKEN_HERE
```

### 2. Tester localement

```bash
# Installer les dépendances
pip install -r requirements.txt

# Démarrer Vercel CLI localement
npm install -g vercel
vercel dev
```

Accès: `http://localhost:3000`

### 3. Déployer sur Vercel

```bash
# Première fois
vercel

# Ou si vous avez déjà un projet
vercel --prod
```

## 🔧 Endpoints API

### POST `/api/chat`

**Request:**
```json
{
  "message": "Quelle est la différence entre une action et un obligation?"
}
```

**Response (Success):**
```json
{
  "reply": "Une action représente une part de propriété d'une entreprise... 📊"
}
```

**Response (Error):**
```json
{
  "error": "Message requis"
}
```

## 📦 Dépendances

| Package | Utilisé pour |
|---------|-------------|
| `requests` | Appels HTTP vers l'API Hugging Face |

*Zéro dépendance backend lourd (pas Flask, pas FastAPI)*

## 🔐 Variables d'environnement

| Variable | Requis | Description |
|----------|--------|-------------|
| `HF_API_TOKEN` | ✅ | Token Hugging Face (https://huggingface.co/settings/tokens) |

### Définir dans Vercel

```bash
vercel env add HF_API_TOKEN
# Paster le token quand demandé
```

Ou via le dashboard Vercel: `Project Settings → Environment Variables`

## ⚙️ Configuration Vercel

**vercel.json** définit:
- **Builds**: API Python serverless + assets statiques
- **Routes**: `/api/*` → Python handler, `/*` → frontend static
- **Headers**: CORS inclus dans le handler

## 🧠 Modèle IA utilisé

- **Modèle**: `HuggingFaceTB/SmolLM-1.7B-Instruct`
- **Type**: Instruct tuned, léger et rapide
- **Prompt system**: Fintech expert avec disclaimers légaux

Modèles alternatifs:
- `mistralai/Mistral-7B-Instruct-v0.2`
- `meta-llama/Llama-2-7b-chat`
- `NousResearch/Nous-Hermes-2-7b`

*Changer dans `api/chat.py` ligne 6*

## 🛡️ Sécurité

✅ **Implémenté:**
- Token API en variables d'environnement (jamais dans le code)
- CORS headers explicites
- Validation des entrées (message non-vide)
- Erreur handling robuste
- Timeout 45s sur appels externes

⚠️ **Important:**
- Ne jamais committer `.env`
- Utiliser `.env.example` pour documenter les variables
- Token dans Vercel secrets, pas dans le code

## 📱 Responsive

- Desktop: chat complet
- Mobile: optimisé pour petits écrans
- Scroll auto vers les nouveaux messages
- Input auto-resize

## 🎯 Endpoints

| Chemin | Méthode | Description |
|--------|---------|-------------|
| `/api/chat` | POST | Chat principal fintech |
| `/` | GET | Serve index.html |
| `/style.css` | GET | Serve styles |
| `/script.js` | GET | Serve logique client |

## 🚨 Troubleshooting

### "API token non configuré"
→ Ajouter `HF_API_TOKEN` dans Vercel environment variables

### "Erreur API externe"
→ Token invalide ou quota HF dépassé
→ Vérifier sur https://huggingface.co/settings/tokens

### CORS error en local
→ `vercel dev` proxifie correctement
→ Si erreur persiste, vérifier les headers dans `api/chat.py`

### Modèle lent
→ Augmenter `max_new_tokens` = réponses plus longues = plus lent
→ Décrire `temperature` pour moins de créativité (→ plus rapide)

## 📚 Resources

- [Vercel Python Runtime](https://vercel.com/docs/functions/python)
- [Hugging Face Inference API](https://huggingface.co/inference-api)
- [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables)

## ⚖️ Disclaimer

Cet assistant n'est **pas** un conseiller financier professionnel. Les réponses sont générales et informatives uniquement. Consultez un expert qualifié pour des décisions financières importantes.

---

**Production-Ready** ✅ Prêt pour déploiement Vercel en 5 minutes
