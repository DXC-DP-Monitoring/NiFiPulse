
import csv
import random
import datetime
import time

# configuration
OUTPUT_CSV_FILE = "ram_metrics1.csv"
TICK_INTERVAL_SECONDS = 5  

def run_simulation():
    
    
    print(f"Début de la simulation RAM")
    print(f"Fichier de sortie : {OUTPUT_CSV_FILE}")
   
    print("!!!!Appuyez sur Ctrl+C pour arrêter la simulation!!!!")

    # définition des en-têtes du fichier CSV
    fieldnames = ["timestamp_utc", "ram_percent"]
    
    try:
        
        # mode='w' : write pour créer/écraser le fichier au démarrage.
        with open(OUTPUT_CSV_FILE, mode='w', newline='', encoding='utf-8') as csv_file:

         # Initialise un DictWriter pour mapper les dictionnaires sur les lignes du fichier CSV.
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            # Écriture d'en-tête
            writer.writeheader()
            print("En-tête du fichier CSV créé.")
            
            # Génération et écriture des données
            while True:
                current_timestamp = datetime.datetime.utcnow().isoformat()
                ram_percent = round(random.uniform(30.0, 85.0), 2)
                
                # Préparer la nouvelle ligne 
                new_row = {
                    "timestamp_utc": current_timestamp,
                    "ram_percent": ram_percent
                }
                print(f"Génération: {new_row}")
                
        
                writer.writerow(new_row)
                
                # Forcer l'écriture immédiate sur le disque
                csv_file.flush()
                
                time.sleep(TICK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nInterruption détectée (Ctrl+C)>>> Arrêt de la simulation.")
    
    finally:
        print(f" Fin de la simulation Les données sont enregistrées dans {OUTPUT_CSV_FILE}. ---")

if __name__ == "__main__":
    run_simulation()