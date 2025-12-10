import time
import requests
import csv
import os
import nifipulse.config as config
from datetime import datetime
from importlib.resources import files
from nifipulse.utils import abs_ff_path, path_tofolder, _csv_has_rows
from nifipulse.data_normalisation import process_data
from nifipulse.load_postgres import load_postgres

def nifipulse(poll_count=10, interval=5):
    """
    poll_count: number of cycles to poll (0 = run forever)
    interval: seconds to wait between cycles
    """
    if not path_tofolder(abs_ff_path(config.env.RESULTS_DIR)):
        print("Creating results directory...")
        os.makedirs(abs_ff_path(config.env.RESULTS_DIR), exist_ok=True)
    
    # Load metrics file from package data
    try:
        metrics_text = files("nifipulse").joinpath("metrics_list.txt").read_text(encoding="utf-8")
        metrics = [line.strip() for line in metrics_text.splitlines() if line.strip()]
    except Exception as e:
        print(f"Could not load metrics_list.txt from package: {e}")
        metrics = []

    # Poll and write CSV
    poll_metrics(interval, save_csv=True, metrics=metrics, count=poll_count)

    # Only normalize if CSV has at least one data row
    if _csv_has_rows(config.env.CSV_SINK):
        process_data()
    else:
        print("No polled rows written; skipping normalization.")
        return

    #Only load to Postgres if cleaned data exists
    if _csv_has_rows(config.env.CLEAN_DATA):
        load_postgres(config.env.CLEAN_DATA)
    else:
        print("No cleaned data to load into Postgres; skipping load.")
        return

def poll_metrics(interval=None, save_csv=True, metrics=None, count=10):
    if metrics is None or not metrics:
        print("No metrics provided to poll.")
        return
    
    """Poll Prometheus periodically and log metrics."""
    # Initialize CSV with headers
    if save_csv:
        with open(config.env.CSV_SINK, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "instance", "metric_name", "component_name", "value"])
            writer.writeheader()

    cycle = 0
    while True:
        cycle += 1
        timestamp = datetime.now().isoformat()

        for metric_name in metrics:
            try:
                # Query Prometheus API for each metric
                response = requests.get(config.env.PROM_URL, params={"query": metric_name})
                response.raise_for_status()
                data = response.json()
                results = data.get("data", {}).get("result", [])

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
                        with open(config.env.CSV_SINK, "a", newline="") as f:
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
        
        # Stop if we’ve reached the requested number of cycles (unless 0 = forever)
        if count and cycle >= count:
            break
        
        time.sleep(interval)
    print("\nPolling complete.")

