import csv
import os
import tempfile
import builtins
import pytest

import nifipulse.config as config
from nifipulse.data_normalisation import process_data   


# -----------------------------
# Helper to create temp CSV data
# -----------------------------
def create_csv(path, rows):
    fieldnames = ["timestamp", "instance", "metric_name", "component_name",
                  "component_type", "component_id", "value"]

    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


# -----------------------------
# TEST: process_data filters, maps, converts and writes results
# -----------------------------
def test_process_data(tmp_path, monkeypatch):
    # Temporary paths
    input_csv = tmp_path / "input.csv"
    output_csv = tmp_path / "clean.csv"

    # Fake rows
    rows = [
        # 👎 should be filtered (value = 0 AND metric starts with nifi_amount)
        {
            "timestamp": "2025-01-01T00:00:00Z",
            "instance": "nifi1",
            "metric_name": "nifi_amount_flowfiles_received",
            "component_name": "ProcessorA",
            "component_type": "PROCESSOR",
            "component_id": "abc123",
            "value": "0"
        },
        # 👍 should be kept and mapped
        {
            "timestamp": "2025-01-01T00:01:00Z",
            "instance": "nifi1",
            "metric_name": "nifi_amount_bytes_read",
            "component_name": "ProcessorB",
            "component_type": "PROCESSOR",
            "component_id": "xyz999",
            "value": "150"
        }
    ]

    create_csv(input_csv, rows)

    # Override config.env paths
    monkeypatch.setattr(config, "env", type("E", (), {
        "CSV_SINK": str(input_csv),
        "CLEAN_DATA": str(output_csv)
    }))

    # Run the function
    process_data()

    # ----------- Validate output CSV -----------
    assert output_csv.exists(), "Output file should be created"

    with open(output_csv, encoding='utf-8') as f:
        reader = list(csv.DictReader(f))

    # One row should remain
    assert len(reader) == 1

    row = reader[0]

    # Validate correct mapping
    assert row["metric_name"] == "bytes_read"

    # Validate unit detection
    assert row["original_unit"] == "bytes"

    # Validate numeric conversion
    assert row["value"] == "150.0"

    # Validate ID propagation
    assert row["unique_id"] == "xyz999"

    # Validate timestamp copy
    assert row["timestamp_utc"] == "2025-01-01T00:01:00Z"
