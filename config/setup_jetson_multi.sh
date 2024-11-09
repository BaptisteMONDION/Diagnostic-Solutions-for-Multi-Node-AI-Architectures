#!/bin/bash

# Mettre à jour les packages et installer les dépendances de base
echo "Mise à jour des packages..."
sudo apt update && sudo apt upgrade -y

# Installer Node Exporter pour Prometheus
echo "Installation de Node Exporter..."
wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-armv7.tar.gz
tar -xvzf node_exporter-1.3.1.linux-armv7.tar.gz
cd node_exporter-1.3.1.linux-armv7
./node_exporter &

# Installer CUDA et TensorFlow (ou PyTorch selon le besoin)
echo "Installation de CUDA..."
sudo apt-get install nvidia-cuda-toolkit -y

echo "Installation de TensorFlow..."
pip install tensorflow

# Installer les dépendances pour surveiller la consommation d'énergie (INA3221)
echo "Installation des dépendances INA3221..."
sudo apt-get install python-smbus -y
pip install adafruit-circuitpython-ina3221

# Installer Prometheus Node Exporter
echo "Configuration de Node Exporter..."
sudo cp node_exporter /usr/local/bin
sudo nohup /usr/local/bin/node_exporter &

# Installer stunnel pour sécuriser les connexions SSH
echo "Installation de Stunnel..."
sudo apt-get install stunnel4 -y

# Configurer stunnel (si nécessaire, fichier de config à ajouter ici)
# sudo cp /path_to_stunnel_config_file /etc/stunnel/stunnel.conf

# Ajouter le service stunnel pour démarrage automatique (si nécessaire)
# sudo systemctl enable stunnel4

# Configurer SSH
echo "Configuration de SSH..."
sudo systemctl enable ssh
sudo systemctl start ssh

# Installer Prometheus pour surveiller plusieurs Jetson Nano
echo "Installation de Prometheus..."
sudo apt install prometheus -y
sudo systemctl start prometheus
sudo systemctl enable prometheus

# Installer Grafana (sur serveur central uniquement)
echo "Installation de Grafana (serveur central)..."
# Sur le serveur central, exécutez :
# sudo apt install grafana -y
# sudo systemctl start grafana-server
# sudo systemctl enable grafana-server

# Configuration de Prometheus sur le serveur central pour récupérer les données de tous les Jetson
echo "Configurer Prometheus sur le serveur central..."
# Modifiez /etc/prometheus/prometheus.yml sur le serveur pour inclure toutes les IP des Jetson Nano
# Exemple :
#   static_configs:
#     - targets:
#       - '172.18.2.142:9100'
#       - '172.18.2.143:9100'
#       - '172.18.2.144:9100'
#       - ...
echo "Configuration terminée pour 10 Jetson Nano."
