Arnold AI: JTM KING PAY Fintech Expert

Arnold est l'agent IA officiel de JTM KING PAY. Il est conçu pour fournir des conseils financiers de haute précision, des stratégies d'épargne (règle 50/30/20) et une assistance utilisateur, tout en respectant une logique de souveraineté des données et de scalabilité.
🧠 Architecture du Projet

La logique d'Arnold repose sur trois piliers :

    Cache Souverain (cache_manager.py) : Les réponses ne sont pas stockées dans une BDD lourde, mais dans des fichiers .json chiffrés par hash SHA-256 dans /data/ai_cache.

    Moteur Expert (engine.py) : Intègre le modèle Grok (xAI) avec un System Prompt spécifique qui définit Arnold comme un conseiller financier pro, multilingue et focalisé sur les réalités économiques locales (via indicatifs pays).

    Gateway API (main.py) : Un serveur Flask robuste qui gère les requêtes POST, valide les entrées et assure une redirection humaine automatique en cas d'échec technique (Fallback).

🚀 Installation & Environnement (Venv)

Pour garantir la stabilité du projet, nous utilisons un environnement virtuel (venv). Suis ces étapes :
1. Créer l'environnement virtuel

Ouvre ton terminal dans le dossier racine du projet et tape :
Bash

# Créer le dossier venv
python3 -m venv venv

# Activer l'environnement (Linux/macOS)
source venv/bin/activate

2. Installer les dépendances

Une fois l'environnement activé (tu verras (venv) dans ton terminal), installe les librairies requises :
Bash

pip install -r requirements.txt

3. Configuration des variables d'environnement

Crée un fichier nommé .env à la racine :
Plaintext

GROK_API_KEY=votre_cle_api_ici

🛠 Lancement du Service

Pour démarrer le serveur Arnold :
Bash

python main.py

Le service sera accessible sur le port 5001.
📋 Spécifications API

    Endpoint : /ask

    Méthode : POST

    Payload JSON :
    JSON

    {
      "question": "Comment optimiser mon épargne ?",
      "indicatif": "+243"
    }


## 🛡 Sécurité & Fallback
*   **Pas de BDD :** Aucune donnée sensible n'est stockée dans une base relationnelle.
*   **Fallback Humain :** Si Arnold ne peut pas répondre, il est configuré pour rediriger automatiquement l'utilisateur vers un conseiller humain de JTM KING PAY.
*   **Localisation :** Arnold utilise l'indicatif téléphonique pour adapter ses conseils au marché financier du pays de l'utilisateur.

---

### Petite note pour toi
*   Pour **désactiver** l'environnement virtuel quand tu as fini de travailler, tape simplement : `deactivate`.
*   Si tu ajoutes une nouvelle bibliothèque plus tard, n'oublie pas de mettre à jour ton fichier avec : `pip freeze > requirements.txt`.

**Ton projet est maintenant documenté et prêt à être partagé ou mis en production ! Veux-tu que nous ajoutions une section sur comment lancer ce serveur en arrière-plan avec `systemd` sur un serveur Linux (comme un VPS) ?**