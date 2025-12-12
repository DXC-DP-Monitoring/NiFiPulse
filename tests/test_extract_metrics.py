import pytest
from unittest.mock import patch, MagicMock
import nifipulse.extract_metrics as em
import nifipulse.config as config

# FIXTURE POUR MOCKER config.env + CRÉER results/
@pytest.fixture
def mock_env(tmp_path):
    # Création du dossier results/ avant les tests
    results_dir = tmp_path / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    class Env:
        RESULTS_DIR = str(results_dir)
        CSV_SINK = str(results_dir / "raw.csv")
        CLEAN_DATA = str(results_dir / "clean.csv")
        PROM_URL = "http://fake-prometheus/api"

    with patch.object(config, "env", Env):
        yield Env


# TESTS poll_metrics()

def test_poll_metrics_no_metrics(mock_env):
    with patch("builtins.print") as mock_print:
        em.poll_metrics(metrics=[])
        mock_print.assert_called_with("No metrics provided to poll.")



def test_poll_metrics_calls_prometheus_and_writes_csv(mock_env):
    metrics = ["nifi_metric"]
    # Mock réponse Prometheus
    fake_resp = MagicMock()
    fake_resp.raise_for_status.return_value = None
    fake_resp.json.return_value = {
        "data": {
            "result": [{
                "metric": {"instance": "nifi:9092", "component_name": "UpdateAttribute", "component_id": "cid1", "component_type": "PROCESSOR"},
                "value": [1700000000, "5"]
            }]
        }
    }

    # Patch where it's used
    with patch("nifipulse.extract_metrics.requests.get", return_value=fake_resp):
        em.poll_metrics(metrics=metrics, interval=0, count=1)

    # Vérifier écriture du CSV
    with open(config.env.CSV_SINK) as f:
        lines = f.readlines()

    assert len(lines) == 2  # header + data line
    assert "UpdateAttribute" in lines[1]
    assert ",5" in lines[1]


# TESTS nifipulse()

def test_nifipulse_no_rows(mock_env):
    with patch("nifipulse.extract_metrics.path_tofolder", return_value=True), \
         patch("nifipulse.extract_metrics.files") as mock_files, \
         patch("nifipulse.extract_metrics.poll_metrics") as mock_poll, \
         patch("nifipulse.extract_metrics._csv_has_rows", return_value=False), \
         patch("builtins.print") as mock_print:
        mock_files.return_value.joinpath.return_value.read_text.return_value = "metric1"
        em.nifipulse(poll_count=1, interval=0)
        mock_poll.assert_called_once()
        mock_print.assert_any_call("No polled rows written; skipping normalization.")

   

def test_nifipulse_full_flow(mock_env):
    with patch("nifipulse.extract_metrics.path_tofolder", return_value=True), \
         patch("nifipulse.extract_metrics.files") as mock_files, \
         patch("nifipulse.extract_metrics._csv_has_rows", side_effect=[True, True]), \
         patch("nifipulse.extract_metrics.process_data") as mock_process, \
         patch("nifipulse.extract_metrics.load_postgres") as mock_pg, \
         patch("nifipulse.extract_metrics.poll_metrics"):
        mock_files.return_value.joinpath.return_value.read_text.return_value = "metricX"
        em.nifipulse(poll_count=1, interval=0)
        mock_process.assert_called_once()
        mock_pg.assert_called_once()

   
