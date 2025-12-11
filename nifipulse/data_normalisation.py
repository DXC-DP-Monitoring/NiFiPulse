import csv
import hashlib
import nifipulse.config as config


METRIC_MAPPING = {
    "nifi_amount_flowfiles_received": "flowfiles_received",
    "nifi_amount_flowfiles_sent": "flowfiles_sent",
    "nifi_amount_flowfiles_transferred": "flowfiles_transferred",
    "nifi_amount_flowfiles_removed": "flowfiles_removed",
    "nifi_amount_bytes_read": "bytes_read",
    "nifi_amount_bytes_written": "bytes_written",
    "nifi_amount_bytes_sent": "bytes_sent",
    "nifi_amount_bytes_received": "bytes_received"
}

def process_data():
    print(f" Démarrage du traitement de {config.env.CSV_SINK} ")
    
    stats = {"total": 0, "kept": 0, "filtered": 0}
    
    try:
        with open(config.env.CSV_SINK, 'r', encoding='utf-8') as f_in, \
             open(config.env.CLEAN_DATA, 'w', encoding='utf-8', newline='') as f_out:
            
            reader = csv.DictReader(f_in)
            
            # On définit les nouvelles colonnes du fichier propre
            fieldnames = [
                'unique_id',        # ID de déduplication
                'timestamp_utc',    # Timestamp standardisé
                'instance',         # Instance
                'metric_name',      # Nom mappé
                'component_name',   # Nom original
                'component_type',   # Enrichissement
                'value',            # Valeur typée
                'original_unit'     # Unité déduite
            ]
            
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                stats["total"] += 1
                
                #  CONVERSION DE TYPES 
                try:
                    raw_value = float(row['value'])
                except ValueError:
                    raw_value = 0.0
                
                #  FILTRAGE (Nettoyage)
                # Si c'est une métrique de flux ("amount") et qu'elle vaut 0, on jette.
                if raw_value == 0 and "nifi_amount" in row['metric_name']:
                    stats["filtered"] += 1
                    continue # On passe à la ligne suivante, celle-ci est ignorée
                
                # MAPPING DES NOMS 
                raw_metric = row['metric_name']
                clean_metric = METRIC_MAPPING.get(raw_metric, raw_metric) # Si pas dans la liste, garde l'original
                
                # Déduction de l'unité
                unit = "count"
                if "bytes" in clean_metric: unit = "bytes"
                
                #  ENRICHISSEMENT 
                comp_name = row['component_name']
                comp_type = row['component_type']
                
                # Conversion Timestamp (Nettoyage format ISO)
                
                ts_raw = row['timestamp']
                
                #  DEDUPLICATION (Génération ID unique) 
                unique_id = row['component_id']
                
                # Écriture de la ligne propre
                writer.writerow({
                    'unique_id': unique_id,
                    'timestamp_utc': ts_raw, # Déjà en ISO dans la sourcce c'est OK
                    'instance': row['instance'],
                    'metric_name': clean_metric,
                    'component_name': comp_name,
                    'component_type': comp_type,
                    'value': raw_value,     # Stocké comme nombre
                    'original_unit': unit
                })
                stats["kept"] += 1

    except FileNotFoundError:
        print(f"Erreur : Le fichier {config.env.CSV_SINK} n'existe pas.")
        return

    print(" Traitement terminé ")
    print(f"Lignes lues      : {stats['total']}")
    print(f"Lignes filtrées  : {stats['filtered']} (Zeros inutiles)")
    print(f"Lignes gardées   : {stats['kept']} (Sauvegardées dans {config.env.CLEAN_DATA})")
    print(f"Taux de réduction: {round((stats['filtered']/stats['total'])*100, 1)}%")