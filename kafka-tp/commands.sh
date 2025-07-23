#!/bin/bash

# Construire l'image
echo "Construction de l'image..."
docker build -t my_kafka .

# Lancer le conteneur
echo "Lancement du conteneur..."
docker run -d --name my_kafka_run \
--env-file .env \
-p 9092:9092 \
my_kafka

# Attendre que Kafka soit prêt
echo "Attente du démarrage de Kafka..."
sleep 10

# Lister les topics
echo "Topics disponibles:"
docker exec -it my_kafka_run kafka-topics.sh --bootstrap-server localhost:9092 --list

# Créer un topic de test
echo "Création du topic 'test'..."
docker exec -it my_kafka_run kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test --partitions 1 --replication-factor 1

echo "Setup terminé ! Utilisez les commandes suivantes:"
echo "- Producteur: docker exec -it my_kafka_run kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test"
echo "- Consommateur: docker exec -it my_kafka_run kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning"
