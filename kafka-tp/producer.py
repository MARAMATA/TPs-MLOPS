from confluent_kafka import Producer  # Importe la classe Producer de la bibliothèque Kafka Confluent
import time  # Pour faire des pauses entre les envois

# Configuration de la connexion au broker Kafka
conf = {
   'bootstrap.servers': 'localhost:9092'  # Adresse du serveur Kafka (ici local)
}

producer = Producer(conf)  # Crée un producteur Kafka avec cette configuration
# Nom du topic dans lequel on va envoyer les messages
topic = "my_first_topic"

# Fonction appelée quand la livraison d'un message est confirmée ou en erreur
def delivery_report(err, msg):
   if err is not None:  # Si erreur lors de l'envoi
       print(f"Message delivery failed: {err}")
   else:
       # Confirmation que le message est bien envoyé (topic + partition)
       print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Envoi de 10 messages avec un délai d'1 seconde entre chaque
for i in range(100):
   message = f"Message numéro {i}"  # Le contenu du message à envoyer
   # Envoie le message dans le topic, avec la fonction callback pour le suivi
   producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
   producer.poll(0)  # Permet de déclencher les callbacks de livraison en attente
   time.sleep(1)  # Pause de 1 seconde entre chaque message

producer.flush()
