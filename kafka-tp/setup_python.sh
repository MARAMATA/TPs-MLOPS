#!/bin/bash

echo "Installation des dépendances Python..."
pip install -r requirements.txt

echo "Création du topic 'my_first_topic'..."
docker exec -it my_kafka_run kafka-topics.sh --bootstrap-server localhost:9092 --create --topic my_first_topic --partitions 1 --replication-factor 1

echo "Setup terminé !"
echo ""
echo "Pour tester :"
echo "1. Dans un terminal : python consumer.py"
echo "2. Dans un autre terminal : python producer.py"
