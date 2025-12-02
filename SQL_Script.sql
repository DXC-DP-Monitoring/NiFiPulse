
CREATE DATABASE metrics_db;


-- 1. TABLE INSTANCE
CREATE TABLE IF NOT EXISTS dim_instance (
    instance_id SERIAL PRIMARY KEY,
    instance_name VARCHAR(255) UNIQUE NOT NULL
);

-- 2. TABLE METRIC
CREATE TABLE IF NOT EXISTS dim_metric (
    metric_id SERIAL PRIMARY KEY,
    metric_name VARCHAR(255) UNIQUE NOT NULL,
    original_unit VARCHAR(50)
);

-- 3. TABLE COMPONENT
CREATE TABLE IF NOT EXISTS dim_component (
    component_id SERIAL PRIMARY KEY,
    component_name VARCHAR(255) NOT NULL,
    component_type VARCHAR(100) NOT NULL,
    UNIQUE (component_name, component_type)
);

-- 4. TABLE DATE
CREATE TABLE IF NOT EXISTS dim_date (
    date_id SERIAL PRIMARY KEY,
    timestamp_utc TIMESTAMPTZ NOT NULL UNIQUE,
    year INT,
    month INT,
    day INT,
    hour INT,
    minute INT,
    second INT
);

-- 5. FACT TABLE
CREATE TABLE IF NOT EXISTS fact_metrics (
    fact_id SERIAL PRIMARY KEY,
    date_id INT REFERENCES dim_date(date_id),
    instance_id INT REFERENCES dim_instance(instance_id),
    metric_id INT REFERENCES dim_metric(metric_id),
    component_id INT REFERENCES dim_component(component_id),
    value DOUBLE PRECISION,
    UNIQUE (date_id, instance_id, metric_id, component_id)
);
