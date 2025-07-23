# M2DSIA Web Application

Application web pour la gestion des utilisateurs M2DSIA avec FastAPI, SQLAlchemy et Pydantic.

## 🏗️ Structure du Projet

```
m2dsia_web_app/
├── api/
│   ├── __init__.py
│   └── main.py              # API FastAPI
├── db/
│   ├── __init__.py
│   ├── connexion.py         # Configuration base de données
│   └── crud.py              # Opérations CRUD
├── models/
│   ├── __init__.py
│   └── models.py            # Modèles SQLAlchemy
├── schemas/
│   ├── __init__.py
│   └── schemas.py           # Schémas Pydantic
├── logger/
│   ├── __init__.py
│   ├── filters.py           # Filtres de logging
│   └── logging_config.yaml  # Configuration logging
├── tests/
│   └── main.py              # Tests unitaires
├── logs/                    # Dossier des logs (créé automatiquement)
├── create_database.py       # Script création base de données
├── setup_database.py        # Script setup complet
├── requirements.txt         # Dépendances Python
└── README.md               # Ce fichier
```

## 🚀 Installation et Setup

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd m2dsia_web_app
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Créer la base de données

```bash
# Option 1: Création simple de la base
python create_database.py

# Option 2: Setup complet avec données de test
python setup_database.py
```

### 4. Lancer l'API

```bash
# Depuis le dossier racine
python api/main.py

# Ou avec uvicorn
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Tester l'installation

```bash
python tests/main.py
```

## 🔧 Configuration

### Base de données

* **Host** : `m2-dsia.cfuik82swe2y.eu-central-1.rds.amazonaws.com`
* **Base** : `m2dsia_maramata`
* **Port** : `3306`
* **Utilisateur** : `root`

### Endpoints API

#### 📍 Endpoints principaux

| Méthode | Endpoint    | Description              |
| -------- | ----------- | ------------------------ |
| `GET`  | `/`       | Page d'accueil           |
| `GET`  | `/health` | Vérification santé API |
| `GET`  | `/docs`   | Documentation Swagger    |

#### 👥 Gestion des utilisateurs

| Méthode   | Endpoint                        | Description                                    |
| ---------- | ------------------------------- | ---------------------------------------------- |
| `POST`   | `/users/`                     | Créer un utilisateur                          |
| `GET`    | `/users/`                     | Lister tous les utilisateurs (avec pagination) |
| `GET`    | `/users/all`                  | Lister tous les utilisateurs                   |
| `GET`    | `/users/active`               | Lister les utilisateurs actifs                 |
| `GET`    | `/users/{user_id}`            | Obtenir un utilisateur par ID                  |
| `GET`    | `/users/email/{email}`        | Obtenir un utilisateur par email               |
| `GET`    | `/users/class/{classe}`       | Obtenir les utilisateurs par classe            |
| `PUT`    | `/users/{user_id}`            | Mettre à jour un utilisateur                  |
| `DELETE` | `/users/{user_id}`            | Supprimer un utilisateur                       |
| `PATCH`  | `/users/{user_id}/deactivate` | Désactiver un utilisateur                     |

## 📊 Modèle de données

### Utilisateur

```python
{
    "id": int,                    # ID auto-incrémenté
    "email": str,                 # Email unique
    "nom": str,                   # Nom de famille
    "prenom": str,                # Prénom
    "classe": str,                # Classe (ex: "MLOps 2025")
    "is_active": bool,            # Statut actif
    "created_at": datetime,       # Date de création
    "updated_at": datetime        # Date de mise à jour
}
```

## 🧪 Tests

### Lancer les tests

```bash
python tests/main.py
```

### Tests inclus

* ✅ Création d'utilisateur
* ✅ Récupération d'utilisateur
* ✅ Mise à jour d'utilisateur
* ✅ Désactivation d'utilisateur
* ✅ Filtrage par classe
* ✅ Utilisateurs actifs seulement

## 📝 Logging

Les logs sont automatiquement créés dans le dossier `logs/`:

* `m2dsia_app.log` : Logs généraux
* `m2dsia_errors.log` : Erreurs uniquement

### Configuration logging

* Filtrage des données sensibles
* Rotation des logs
* Niveaux configurables

## 🔍 Utilisation

### Créer un utilisateur

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "nouvel.utilisateur@isi.com",
       "nom": "Utilisateur",
       "prenom": "Nouveau",
       "classe": "MLOps 2025"
     }'
```

### Lister tous les utilisateurs

```bash
curl -X GET "http://localhost:8000/users/"
```

### Obtenir un utilisateur par email

```bash
curl -X GET "http://localhost:8000/users/email/nouvel.utilisateur@isi.com"
```

## 🚨 Dépannage

### Erreur de connexion à la base

1. Vérifier la connectivité réseau
2. Vérifier que l'instance RDS est active
3. Vérifier les groupes de sécurité AWS

### Erreur "Module not found"

```bash
# Ajouter le chemin du projet
export PYTHONPATH="${PYTHONPATH}:/path/to/m2dsia_web_app"
```

### Problèmes de dépendances

```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

## 🔧 Développement

### Ajouter de nouvelles fonctionnalités

1. Modifier les modèles dans `models/models.py`
2. Mettre à jour les schémas dans `schemas/schemas.py`
3. Ajouter les opérations CRUD dans `db/crud.py`
4. Créer les endpoints dans `api/main.py`
5. Ajouter les tests dans `tests/main.py`

### Variables d'environnement (recommandé)

Créer un fichier `.env` :

```env
DB_HOST=m2-dsia.cfuik82swe2y.eu-central-1.rds.amazonaws.com
DB_USER=root
DB_PASSWORD=rootM2dsia
DB_NAME=m2dsia_maramata
DB_PORT=3306
```

## 📚 Ressources

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
* [Pydantic Documentation](https://docs.pydantic.dev/)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commit les modifications
4. Push vers la branche
5. Créer une Pull Request

## 📄 License

Ce projet est sous licence MIT.
