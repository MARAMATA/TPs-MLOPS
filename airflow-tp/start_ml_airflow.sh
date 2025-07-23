#!/bin/bash

echo "🚀 Démarrage d'Airflow avec DAGs ML/IA"
echo "====================================="

# Vérifier que Docker est démarré
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas démarré. Démarrez Docker d'abord."
    exit 1
fi

# Tester les DAGs avant de démarrer
echo "🧪 Test des DAGs..."
python3 test_dags.py
if [ $? -ne 0 ]; then
    echo "⚠️ Problèmes détectés dans les DAGs, mais continuons..."
fi

# Arrêter les anciens conteneurs s'ils existent
echo "🛑 Arrêt des anciens conteneurs..."
docker-compose down 2>/dev/null

# Démarrer les services
echo "🚀 Démarrage d'Airflow..."
docker-compose up -d

# Attendre que les services démarrent
echo "⏳ Attente du démarrage des services..."
sleep 30

# Vérifier le statut
echo "📊 Vérification du statut..."
docker-compose ps

echo ""
echo "🎉 Airflow est prêt!"
echo "�� Interface web: http://localhost:8080"
echo "👤 Identifiants: admin / admin"
echo ""
echo "📋 DAGs disponibles:"
echo "   • ml_pipeline_titanic - Pipeline ML classique"
echo "   • advanced_ai_sentiment_pipeline - Analyse de sentiment"
echo "   • computer_vision_pipeline - Classification d'images"
echo "   • ml_monitoring_dashboard - Monitoring des pipelines"
echo ""
echo "💡 Conseils:"
echo "   1. Commencez par activer 'ml_pipeline_titanic'"
echo "   2. Attendez qu'il se termine avant de lancer les autres"
echo "   3. Surveillez les logs en cas de problème"
echo ""

# Fonction pour surveiller les logs
read -p "Voulez-vous surveiller les logs en temps réel? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📝 Surveillance des logs (Ctrl+C pour arrêter)..."
    docker-compose logs -f
fi
