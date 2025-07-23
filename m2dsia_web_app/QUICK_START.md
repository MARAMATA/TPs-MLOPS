# 🚀 Démarrage Rapide - M2DSIA Web App

## ⚡ Installation en 5 minutes

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Créer la base de données avec données de test

```bash
python setup_database.py
```

### 3. Lancer l'API

```bash
python api/main.py
```

### 4. Tester l'API

Ouvrir dans le navigateur : http://localhost:8000/docs

## 🎯 Commandes Essentielles

### Créer juste la base de données

```bash
python create_database.py
```

### Tester toutes les fonctionnalités

```bash
python tests/main.py
```

### Lancer avec uvicorn

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Endpoints de Test

### Lister tous les utilisateurs

```bash
curl http://localhost:8000/users/
```

### Créer un utilisateur

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@isi.com",
       "nom": "Test",
       "prenom": "User",
       "classe": "MLOps 2025"
     }'
```

### Santé de l'API

```bash
curl http://localhost:8000/health
```

## 🔧 Résolution Rapide des Problèmes

### Erreur "Module not found"

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Erreur de connexion DB

1. Vérifier la connectivité Internet
2. Vérifier que AWS RDS est accessible
3. Relancer `python create_database.py`

### Port 8000 occupé

```bash
python api/main.py --port 8001
```

## 📊 Résultat Attendu

Après `python setup_database.py` :

```
✓ Database 'm2dsia_maramata' created successfully!
✓ Tables created successfully!
✓ User john.doe@isi.com added successfully!
✓ User jane.smith@isi.com added successfully!
✓ User lipson.soume@isi.com added successfully!
✓ User maramata.student@isi.com added successfully!

✓ Database setup verification:
Total users in database: 4
  - John Doe (john.doe@isi.com) - MLOps 2025
  - Jane Smith (jane.smith@isi.com) - MLOps 2025
  - Lipson Soume (lipson.soume@isi.com) - MLOps 2025
  - Student Maramata (maramata.student@isi.com) - MLOps 2025

🎉 Database setup completed successfully!
```

## 🌐 URLs Importantes

* **API Documentation** : http://localhost:8000/docs
* **API Alternative** : http://localhost:8000/redoc
* **Health Check** : http://localhost:8000/health
* **Tous les utilisateurs** : http://localhost:8000/users/

## ✅ Checklist de Vérification

* [ ] Python 3.7+ installé
* [ ] Dépendances installées (`pip install -r requirements.txt`)
* [ ] Base de données créée (`python setup_database.py`)
* [ ] API lancée (`python api/main.py`)
* [ ] Tests passés (`python tests/main.py`)
* [ ] Documentation accessible (http://localhost:8000/docs)

## 🆘 Aide Rapide

Si quelque chose ne fonctionne pas :

1. **Vérifier Python** : `python --version` (doit être 3.7+)
2. **Vérifier les dépendances** : `pip list | grep fastapi`
3. **Vérifier la DB** : `python create_database.py`
4. **Vérifier l'API** : `curl http://localhost:8000/health`

💡 **Tip** : Utilisez `python setup_database.py` pour une installation complète automatique !
