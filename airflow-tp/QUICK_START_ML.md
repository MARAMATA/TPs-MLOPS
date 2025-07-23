# 🚀 Guide de Démarrage Rapide - DAGs ML/IA

## ⚡ Démarrage en 3 étapes

### 1. Démarrer Airflow
```bash
./start_ml_airflow.sh
```

### 2. Accéder à l'interface
- URL: http://localhost:8080
- Login: admin / admin

### 3. Activer et lancer les DAGs
1. `ml_pipeline_titanic` ← Commencer par celui-ci
2. `advanced_ai_sentiment_pipeline`
3. `computer_vision_pipeline`
4. `ml_monitoring_dashboard`

## 📊 Résultats attendus

Après 30-45 minutes, vous aurez :
- ✅ Modèle ML entraîné (accuracy ~80-85%)
- ✅ Analyse de sentiment sur 1000 posts
- ✅ Classification d'images avec features
- ✅ Dashboard de monitoring complet

## 🔍 Vérification des résultats

```bash
# Vérifier les fichiers générés
ls -la /tmp/ml_pipeline/
ls -la /tmp/ai_pipeline/
ls -la /tmp/cv_pipeline/

# Voir les rapports
cat /tmp/ml_pipeline/final_report.json
cat /tmp/ai_pipeline/ai_insights.json
```

## 🚨 En cas de problème

1. **DAG en erreur** : Regarder les logs dans l'interface Airflow
2. **Packages manquants** : Normal, les DAGs installent automatiquement
3. **Mémoire insuffisante** : Fermer d'autres applications
4. **Docker lent** : Augmenter les ressources Docker

## 🎯 Objectifs pédagogiques

À la fin de ce TP, vous maîtriserez :
- ✅ Orchestration de pipelines ML avec Airflow
- ✅ Preprocessing de données automatisé
- ✅ Entraînement et évaluation de modèles
- ✅ NLP et analyse de sentiment
- ✅ Computer Vision et classification d'images
- ✅ Monitoring et observabilité ML

Bon apprentissage ! 🎉
