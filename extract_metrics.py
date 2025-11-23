import time
import requests
import csv
from datetime import datetime

# Prometheus query API endpoint
PROM_URL = "http://localhost:9090/api/v1/query"

# Load metrics from file (one metric per line)
with open("metrics_list.txt") as f:
    metrics = [line.strip() for line in f if line.strip()]

# Output file
CSV_FILE = "prometheus_metrics_log.csv"

def poll_metrics(interval=5, save_csv=True):
    """Poll Prometheus periodically and log metrics."""
    # Initialize CSV with headers
    if save_csv:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "instance", "metric_name", "component_name", "value"])
            writer.writeheader()

    while True:
        timestamp = datetime.now().isoformat()

        for metric_name in metrics:
            try:
                # Query Prometheus API for each metric
                response = requests.get(PROM_URL, params={"query": metric_name})
                response.raise_for_status()
                data = response.json()

                # Extract data
                results = data.get("data", {}).get("result", [])

                if not results:
                    print(f"[{timestamp}] No data for metric: {metric_name}.")

                print(f"\n[{timestamp}] {len(results)} metrics retrieved")

                for metric in results:
                    labels = metric.get("metric", {})
                    instance = labels.get("instance", "unknown")
                    component_name = labels.get("component_name", "unknown")
                    value = metric.get("value", ["0", "0"])[1]

                    print(f"→ {component_name} ({instance}): {value}")

                    if save_csv:
                        with open(CSV_FILE, "a", newline="") as f:
                            writer = csv.DictWriter(f, fieldnames=["timestamp", "instance", "metric_name", "component_name", "value"])
                            writer.writerow({
                                "timestamp": timestamp,
                                "instance": instance,
                                "metric_name": metric_name,
                                "component_name": component_name,
                                "value": value
                            })

            except Exception as e:
                print(f"[{datetime.now()}] Error: {e}")

            time.sleep(interval)


if __name__ == "__main__":
    poll_metrics(interval=5, save_csv=True)
