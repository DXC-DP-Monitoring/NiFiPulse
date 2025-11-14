import time
import requests
import csv
from datetime import datetime

# -----------------------------
# CONFIGURATION
# -----------------------------
PROM_URL = "http://localhost:9090/api/v1/query"  # URL Prometheus
QUERY = "nifi_amount_items_input"                # La métrique que l'on veut
CSV_FILE = "prometheus_metrics_log.csv"         # Fichier CSV de sortie
POLL_INTERVAL = 5                                # Intervalle en secondes entre chaque poll

# -----------------------------
# FONCTION POUR PULLER LES MÉTRIQUES
# -----------------------------
def poll_metrics(interval=POLL_INTERVAL, save_csv=True):
    """Poll Prometheus périodiquement et sauvegarde les métriques."""
    
    # Initialisation du CSV avec les headers
    if save_csv:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "instance", "component_name", "component_type", "value"])
            writer.writeheader()

    print(f"[INFO] Démarrage de la collecte des métriques toutes les {interval}s...")

    while True:
        try:
            # Interroger l'API Prometheus
            response = requests.get(PROM_URL, params={"query": QUERY})
            response.raise_for_status()
            data = response.json()

            results = data.get("data", {}).get("result", [])
            timestamp = datetime.now().isoformat()

            if not results:
                print(f"[{timestamp}] Aucune métrique trouvée.")
            else:
                print(f"\n[{timestamp}] {len(results)} métriques récupérées :")
                for metric in results:
                    labels = metric.get("metric", {})
                    instance = labels.get("instance", "unknown")
                    component_name = labels.get("component_name", "unknown")
                    component_type = labels.get("component_type", "unknown")
                    value = metric.get("value", ["0", "0"])[1]

                    print(f"→ {component_name} ({component_type}, {instance}) : {value}")

                    # Écriture dans le CSV
                    if save_csv:
                        with open(CSV_FILE, "a", newline="") as f:
                            writer = csv.DictWriter(f, fieldnames=["timestamp", "instance", "component_name", "component_type", "value"])
                            writer.writerow({
                                "timestamp": timestamp,
                                "instance": instance,
                                "component_name": component_name,
                                "component_type": component_type,
                                "value": value
                            })

        except Exception as e:
            print(f"[{datetime.now()}] ERREUR : {e}")

        time.sleep(interval)

# -----------------------------
# EXECUTION DU SCRIPT
# -----------------------------
if __name__ == "__main__":
    poll_metrics()
