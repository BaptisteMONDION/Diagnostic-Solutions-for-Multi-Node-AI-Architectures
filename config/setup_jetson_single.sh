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

# Installer Prometheus (si besoin localement sur un Jetson)
echo "Installation de Prometheus..."
sudo apt install prometheus -y
sudo systemctl start prometheus
sudo systemctl enable prometheus

# Installer et configurer Grafana (si nécessaire sur un serveur)
echo "Installation de Grafana (sur serveur central)..."
# Pour cela, installer Grafana sur le serveur central, pas sur chaque Jetson Nano
# Si nécessaire sur Jetson : 
# sudo apt install grafana -y
# sudo systemctl start grafana-server
# sudo systemctl enable grafana-server

echo "Configuration terminée sur 1 Jetson Nano."
