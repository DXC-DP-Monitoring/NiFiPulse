
import csv
import random
import datetime
import time

# CONFIGURATION 
OUTPUT_CSV_FILE = "ram_nifi_metric.csv"
TICK_INTERVAL_SECONDS = 5  # Un enregistrement toutes les 5 secondes

def run_simulation():
 
    
    print(f"Début de la simulation RAM")
    print(f"Fichier de sortie : {OUTPUT_CSV_FILE}")
    print("!!!!Appuyez sur Ctrl+C pour arrêter proprement!!!!")


    fieldnames = [
        "timestamp_utc",
        "instance",         # Le serveur ou l'instance qui produit la métrique
        "metric_name",      # Le nom de ce que l'on mesure
        "component_name",   # Le composant concerné : RAM
        "value"             # La valeur mesurée
    ]
    
    try:
        with open(OUTPUT_CSV_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
            
            # Initialiser un DictWriter pour mapper nos dictionnaires en csv
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            # Initialiser l'en-tête : une seule fois au début
            writer.writeheader()
            print("En-tête du fichier CSV ")
            
            while True:
                current_timestamp = datetime.datetime.utcnow().isoformat()
                ram_percent_value = round(random.uniform(30.0, 85.0), 2)
                
             
                new_row = {
                    "timestamp_utc": current_timestamp,
                    "instance": "nifi-jvm-instance-01",  # Valeur fixe pour montrer d'où vient la métrique
                    "metric_name": "ram_usage_percent",   # La colonne ram_percent 
                    "component_name": "NiFi_JVM",         # La RAM est une métrique de la JVM (Java Virtual Machine) de NiFi
                    "value": ram_percent_value            # La valeur numérique de notre mesure
                }
                print(f"Génération: {new_row}")
                
               
                writer.writerow(new_row)
                csv_file.flush()
                time.sleep(TICK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n Arrêt de la simulation.")
    
    finally:
        print(f"Fin de la simulation : LesDonnées enregistrées dans {OUTPUT_CSV_FILE}. ---")

if __name__ == "__main__":
    run_simulation()