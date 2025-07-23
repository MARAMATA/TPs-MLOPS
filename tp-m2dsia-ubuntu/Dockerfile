FROM ubuntu:22.04
RUN echo "=== ÉTAPE 1: Configuration de base ==="
ENV DEBIAN_FRONTEND=noninteractive
RUN echo "=== ÉTAPE 2: Mise à jour du système ==="
RUN apt-get update
RUN echo "=== ÉTAPE 3: Installation des paquets ==="
RUN apt-get install -y curl && \
    apt-get clean
RUN echo "=== ÉTAPE 4: Configuration terminée ==="
CMD ["bash"]





