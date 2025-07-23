FROM mysql:8.0.35

# Exposition du port MySQL
EXPOSE 3306

# Copie du script d'initialisation SQL dans le répertoire de démarrage
COPY init.sql /docker-entrypoint-initdb.d/
