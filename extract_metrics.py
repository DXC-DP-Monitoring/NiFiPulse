import time
import requests
import csv
from datetime import datetime

# Prometheus API query
PROM_URL = "http://localhost:9090/api/v1/query?query=nifi_flowfile_in_bytes_total"

# CSV output file 
CSV_FILE = "metrics_log.csv"

def poll_metrics(interval=5, save_csv=True):
    """Poll Prometheus and log metrics."""
    if save_csv:
        # Initialize CSV file with headers
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'instance', 'value'])
            writer.writeheader()

    while True:
        try:
            r = requests.get(PROM_URL)
            r.raise_for_status()
            data = r.json()

            timestamp = datetime.now().isoformat()
            results = data.get('data', {}).get('result', [])

            if not results:
                print(f"[{timestamp}] No metrics found.")
            else:
                print(f"[{timestamp}] --- Sample ---")
                for metric in results[:5]:  # show first 5 metrics for brevity
                    instance = metric['metric'].get('instance', 'unknown')
                    value = metric['value'][1]
                    print(f"{instance} -> {value}")

                    if save_csv:
                        with open(CSV_FILE, 'a', newline='') as f:
                            writer = csv.DictWriter(f, fieldnames=['timestamp', 'instance', 'value'])
                            writer.writerow({'timestamp': timestamp, 'instance': instance, 'value': value})

        except Exception as e:
            print(f"[{datetime.now()}] Error: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    poll_metrics(interval=5, save_csv=True)
