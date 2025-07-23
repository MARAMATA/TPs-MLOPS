from confluent_kafka import Consumer, KafkaException

# Configuration du consumer Kafka
conf = {
   'bootstrap.servers': 'localhost:9092',  # Adresse du broker Kafka
   'group.id': 'mon-groupe-python', # Nom du groupe de consommateurs (gestion offsets)
   'auto.offset.reset': 'earliest' # Lire les sms depuis le début si offset inconnu
}
consumer = Consumer(conf)  # Créer un consommateur Kafka avec cette config
topic = "my_first_topic"       # Le topic à écouter

consumer.subscribe([topic])  # S'abonne au topic
try:
   print("En attente de messages...")
   # Boucle infinie pour écouter les messages en continu
   while True:
       msg = consumer.poll(1.0)  # Attend jusqu'à 1 seconde qu'un message arrive
       if msg is None:
           continue  # Si pas de message reçu, continue à écouter

       if msg.error():
           # En cas d'erreur dans la réception, on lève une exception
           raise KafkaException(msg.error())

       # Si message valide, on affiche son contenu (décodé en UTF-8)
       print(f"Reçu: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
   # Si l'utilisateur interrompt (Ctrl+C), on affiche un message et quitte proprement
   print("Arrêt par l'utilisateur")

finally:
   consumer.close()  # Ferme proprement le consumer (commit offsets, libération ressources)
