# Airflow TP - My-airflow-workspace

## Structure du projet
```
airflow-tp/
├── docker-compose.yml
├── .env
├── dags/
└── README.md
```

## Instructions de démarrage

### Étape 1 : Tester PostgreSQL uniquement
```bash
docker-compose up postgres
```

### Étape 2 : Vérifier les conteneurs
```bash
docker-compose ps
```

### Étape 3 : Arrêter les conteneurs
```bash
docker-compose down
```

### Étape 4 : Lancer tous les services Airflow
```bash
docker-compose up
```

### Étape 5 : Accès à l'interface web
Ouvrez votre navigateur : http://localhost:8080

**Identifiants :**
- Username: admin
- Password: admin

## Services
- **PostgreSQL** : Base de données (port interne 5432)
- **Airflow Webserver** : Interface web (port 8080)
- **Airflow Scheduler** : Planificateur de tâches
- **Airflow Init** : Initialisation et création utilisateur admin

## Notes
- Placez vos DAGs dans le répertoire `dags/`
- Les données PostgreSQL sont persistantes via un volume Docker
- L'utilisateur admin est créé automatiquement
