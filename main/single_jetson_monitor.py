import psutil
import time
import json
import requests
import smbus
from prometheus_client import start_http_server, Gauge

# Variables Prometheus
CPU_USAGE = Gauge('cpu_usage', 'CPU usage of the Jetson Nano')
GPU_USAGE = Gauge('gpu_usage', 'GPU usage of the Jetson Nano')
MEMORY_USAGE = Gauge('memory_usage', 'Memory usage of the Jetson Nano')
ENERGY_CONSUMPTION = Gauge('energy_consumption', 'Energy consumption of the Jetson Nano')

# Fonction de collecte des métriques CPU, mémoire, GPU
def collect_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # Pour GPU usage, vous pouvez utiliser nvidia-smi ou toute autre méthode selon votre configuration
    gpu_usage = get_gpu_usage()

    # Mesure de la consommation d'énergie via INA3221 (assurez-vous d'avoir installé le bon driver)
    energy_consumption = get_energy_consumption()

    # Mettre à jour les métriques
    CPU_USAGE.set(cpu_usage)
    GPU_USAGE.set(gpu_usage)
    MEMORY_USAGE.set(memory_usage)
    ENERGY_CONSUMPTION.set(energy_consumption)

# Fonction pour obtenir l'utilisation GPU (exemple avec nvidia-smi)
def get_gpu_usage():
    try:
        import subprocess
        result = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"], stdout=subprocess.PIPE)
        return float(result.stdout.decode().strip())
    except Exception as e:
        print(f"Erreur lors de la collecte de l'utilisation GPU: {e}")
        return 0.0

# Fonction pour lire la consommation d'énergie via INA3221
def get_energy_consumption():
    try:
        bus = smbus.SMBus(1)
        INA3221_ADDR = 0x40  # Adresse I2C de INA3221
        # Lecture de la consommation d'énergie (les registres doivent être spécifiés selon la datasheet)
        energy = bus.read_word_data(INA3221_ADDR, 0x02)  # Exemple de lecture d'un registre (ajustez selon le capteur)
        return energy / 1000.0  # Conversion en watts (ajustez selon le capteur)
    except Exception as e:
        print(f"Erreur lors de la lecture du capteur INA3221: {e}")
        return 0.0

# Fonction principale pour démarrer la collecte et l'exposition des métriques
def main():
    start_http_server(8000)  # Démarre le serveur Prometheus sur le port 8000
    while True:
        collect_metrics()
        time.sleep(5)  # Collecte toutes les 5 secondes

if __name__ == "__main__":
    main()
