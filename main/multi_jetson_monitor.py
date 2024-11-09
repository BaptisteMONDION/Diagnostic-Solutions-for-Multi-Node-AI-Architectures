import paramiko
import psutil
import time
import json
import requests
from prometheus_client import start_http_server, Gauge

# Variables Prometheus
CPU_USAGE = Gauge('cpu_usage', 'CPU usage of the Jetson Nano')
GPU_USAGE = Gauge('gpu_usage', 'GPU usage of the Jetson Nano')
MEMORY_USAGE = Gauge('memory_usage', 'Memory usage of the Jetson Nano')
ENERGY_CONSUMPTION = Gauge('energy_consumption', 'Energy consumption of the Jetson Nano')

# Paramètres SSH
JETSON_NODES = [
    {"ip": "172.18.2.142", "user": "bmon", "key_file": "/path/to/id_rsa"},
    # Ajoutez les autres Jetson Nano ici si nécessaire
]

# Fonction de connexion SSH
def ssh_connect(node):
    try:
        key = paramiko.RSAKey.from_private_key_file(node["key_file"])
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(node["ip"], username=node["user"], pkey=key)
        return ssh
    except Exception as e:
        print(f"Erreur SSH: {e}")
        return None

# Fonction pour exécuter des commandes sur un Jetson Nano via SSH
def run_ssh_command(ssh, command):
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        return output
    except Exception as e:
        print(f"Erreur lors de l'exécution de la commande SSH: {e}")
        return None

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
        import smbus
        bus = smbus.SMBus(1)
        INA3221_ADDR = 0x40  # Adresse I2C de INA3221
        # Lecture de la consommation d'énergie (les registres doivent être spécifiés selon la datasheet)
        energy = bus.read_word_data(INA3221_ADDR, 0x02)  # Exemple de lecture d'un registre (ajustez selon le capteur)
        return energy / 1000.0  # Conversion en watts (ajustez selon le capteur)
    except Exception as e:
        print(f"Erreur lors de la lecture du capteur INA3221: {e}")
        return 0.0

# Fonction pour récupérer les métriques d'un Jetson Nano distant via SSH
def fetch_metrics_from_node(node):
    ssh = ssh_connect(node)
    if ssh:
        cpu_usage = run_ssh_command(ssh, "cat /proc/cpuinfo")  # Exemple de commande pour obtenir CPU usage
        memory_usage = run_ssh_command(ssh, "free -m")  # Exemple de commande pour obtenir mémoire
        gpu_usage = run_ssh_command(ssh, "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits")
        energy_consumption = run_ssh_command(ssh, "i2cget -y 1 0x40 0x02")  # Lecture de la consommation d'énergie via I2C
        ssh.close()
        
        # Mettez à jour les métriques Prometheus avec les valeurs récupérées
        CPU_USAGE.set(cpu_usage)
        GPU_USAGE.set(gpu_usage)
        MEMORY_USAGE.set(memory_usage)
        ENERGY_CONSUMPTION.set(energy_consumption)

# Fonction principale pour démarrer la collecte et l'exposition des métriques
def main():
    start_http_server(8000)  # Démarre le serveur Prometheus sur le port 8000
    while True:
        for node in JETSON_NODES:
            fetch_metrics_from_node(node)
        time.sleep(5)  # Collecte toutes les 5 secondes

if __name__ == "__main__":
    main()
