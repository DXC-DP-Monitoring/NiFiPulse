import csv
import nifipulse.config as config
from nifipulse.data_normalisation import process_data   
from types import SimpleNamespace


def create_csv(path, rows):
    fieldnames = ["timestamp", "instance", "metric_name", "component_name",
                  "component_type", "component_id", "value"]

    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)



def test_process_data(tmp_path, monkeypatch):
   
    input_csv = tmp_path / "input.csv"
    output_csv = tmp_path / "clean.csv"

    # Fake rows
    rows = [
     
        {
            "timestamp": "2025-01-01T00:00:00Z",
            "instance": "nifi1",
            "metric_name": "nifi_amount_flowfiles_received",
            "component_name": "ProcessorA",
            "component_type": "PROCESSOR",
            "component_id": "abc123",
            "value": "0"
        },
       
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

    cfg = SimpleNamespace(CSV_SINK=str(input_csv), CLEAN_DATA=str(output_csv))
    monkeypatch.setattr(config, "env", cfg, raising=False)

    # Run the function
    process_data()

    # Validate output CSV 
    assert output_csv.exists(), "Output file should be created"

    with open(output_csv, encoding='utf-8') as f:
        reader = list(csv.DictReader(f))

    
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
