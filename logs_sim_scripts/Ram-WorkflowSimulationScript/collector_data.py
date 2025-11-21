import requests
import json
import time
import schedule
import csv
import os

API_ENDPOINT_URL = "http://127.0.0.1:5000/metrics"

CSV_FILE = "collected_ram_workflow_metrics.csv" 
# Les en-têtes 
CSV_HEADERS = [
    'timestamp_utc', 
    'ram_percent',
    'last_workflow_status'
]

def collect_data_from_api():
    #Collecte les données de RAM et de workflow et les enregistre en CSV.
    print(f"collection de (RAM+Workflow) démarrée ({time.ctime()}) ")
    try:
        response = requests.get(API_ENDPOINT_URL, timeout=10)
        response.raise_for_status() 
        
        data = response.json()
        
        print("Données collectées avec succès :")
        print(json.dumps(data, indent=2))
        
        write_to_csv(data)

    except requests.exceptions.RequestException as e:
        print(f"ERREUR : Impossible de collecter {e}")
    except Exception as e:
        print(f"ERREUR inattendue : {e}")

def write_to_csv(data):
    #Écrit une ligne de données (RAM + Workflow) dans le fichier CSV.
    file_exists = os.path.isfile(CSV_FILE)
    
    # Préparation de la ligne des metrics
    row_to_write = [
        data['timestamp_utc'],
        data['metrics']['ram_percent'],
        data['metrics']['last_workflow_status']
    ]

    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            if not file_exists:
                writer.writerow(CSV_HEADERS)
            
            writer.writerow(row_to_write)
            
        print(f"Données enregistrées avec succès dans {CSV_FILE}")

    except Exception as e:
        print(f"ERREUR lors de l'écriture dans le fichier CSV : {e}")


if __name__ == '__main__':
    # On garde un intervalle court pour les tests
    schedule.every(5).seconds.do(collect_data_from_api)
    
    print("Démarrage du collecteur de données (RAM + Workflow).")
    print(f"Les données seront sauvegardées dans le fichier : {CSV_FILE}")
    print("Appuyez sur Ctrl+C pour arrêter.")

    while True:
        schedule.run_pending()
        time.sleep(1)