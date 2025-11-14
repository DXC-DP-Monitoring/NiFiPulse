import time
import requests
import json
from datetime import datetime

# Prometheus query API endpoint
PROM_URL = "http://localhost:9090/api/v1/query"

# The metric you want to pull
QUERY = "nifi_amount_items_input"

# Output file
JSON_FILE = "prometheus_metrics_log.json"

def poll_metrics(interval=5, save_json=True):
    """Poll Prometheus periodically and log metrics in JSON format."""
    
    # Initialize JSON file as an empty list
    if save_json:
        with open(JSON_FILE, "w") as f:
            json.dump([], f)

    while True:
        try:
            # Query Prometheus API
            response = requests.get(PROM_URL, params={"query": QUERY})
            response.raise_for_status()
            data = response.json()

            # Extract data
            results = data.get("data", {}).get("result", [])
            timestamp = datetime.now().isoformat()

            if not results:
                print(f"[{timestamp}] No metrics found.")
            else:
                print(f"\n[{timestamp}] {len(results)} metrics retrieved")

                # Load existing JSON logs
                if save_json:
                    with open(JSON_FILE, "r") as f:
                        existing_data = json.load(f)

                for metric in results:
                    metric_name = QUERY
                    labels = metric.get("metric", {})
                    instance = labels.get("instance", "unknown")
                    component_name = labels.get("component_name", "unknown")
                    value = metric.get("value", ["0", "0"])[1]

                    print(f"→ {component_name} ({instance}): {value}")

                    # Build JSON entry
                    entry = {
                        "timestamp": timestamp,
                        "instance": instance,
                        "metric_name": metric_name,
                        "component_name": component_name,
                        "value": value
                    }

                    # Append new entry and save JSON file
                    if save_json:
                        existing_data.append(entry)
                        with open(JSON_FILE, "w") as f:
                            json.dump(existing_data, f, indent=4)

        except Exception as e:
            print(f"[{datetime.now()}] Error: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    poll_metrics(interval=5, save_json=True)
