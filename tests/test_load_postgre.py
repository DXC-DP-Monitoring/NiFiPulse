import pandas as pd
from unittest.mock import patch, MagicMock
from sqlalchemy.sql.elements import TextClause
from nifipulse.load_postgres import load_postgres


def test_load_postgres_success(tmp_path):
    # Create fake CSV
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(
        "timestamp_utc,instance,metric_name,original_unit,component_name,component_type,value\n"
        "2025-01-01 12:00:00,server1,cpu,%,cpu_component,system,45\n"
    )

    # Mock engine + conn
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.begin.return_value.__enter__.return_value = mock_conn

    #  Fake DataFrames 
    fake_dim_instance = pd.DataFrame({
        "instance_id": [1],
        "instance_name": ["server1"]
    })

    fake_dim_metric = pd.DataFrame({
        "metric_id": [10],
        "metric_name": ["cpu"],
        "original_unit": ["%"]
    })

    fake_dim_component = pd.DataFrame({
        "component_id": [20],
        "component_name": ["cpu_component"],
        "component_type": ["system"]
    })

    fake_dim_date = pd.DataFrame({
        "date_id": [100],
        "timestamp_utc": ["2025-01-01 12:00:00"]
    })

    fake_fact_export = pd.DataFrame({
        "fact_id": [999],
        "timestamp_utc": ["2025-01-01 12:00:00"],
        "instance_name": ["server1"],
        "metric_name": ["cpu"],
        "original_unit": ["%"],
        "component_name": ["cpu_component"],
        "component_type": ["system"],
        "value": [45]
    })

    read_sql_side_effect = [
        fake_dim_instance,
        fake_dim_metric,
        fake_dim_component,
        fake_dim_date,
        fake_fact_export    
    ]

    with patch("nifipulse.load_postgres.create_engine", return_value=mock_engine), \
         patch("nifipulse.load_postgres.pd.read_sql", side_effect=read_sql_side_effect):
        load_postgres(str(csv_file))

    # rom sqlalchemy.sql.elements import TextClause
    texts = []
    for c in mock_conn.execute.call_args_list:
        arg0 = c.args[0]
        if isinstance(arg0, TextClause):
            texts.append(arg0.text)

    assert any("SELECT 1 FROM dim_instance" in sql for sql in texts), "Schema check missing"
    assert any("INSERT INTO dim_instance" in sql for sql in texts)
    assert any("INSERT INTO dim_metric" in sql for sql in texts)
    assert any("INSERT INTO dim_component" in sql for sql in texts)
    assert any("INSERT INTO dim_date" in sql for sql in texts)
    assert any("INSERT INTO fact_metrics" in sql for sql in texts), "Fact insert missing"
