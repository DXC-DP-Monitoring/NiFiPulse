import pandas as pd
from sqlalchemy import create_engine, text

#  Charger le CSV
csv_file = "nifi_metrics_propre.csv"

df = pd.read_csv(csv_file, parse_dates=['timestamp_utc'])
df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'], utc=True)

#  Connexion PostgreSQL

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@postgres:5432/metrics_db"
)


print("- Connexion PostgreSQL OK")

#  INSERT DIMENSIONS
with engine.begin() as conn:

    # dim_instance
    for inst in df['instance'].drop_duplicates():
        conn.execute(text("""
            INSERT INTO dim_instance (instance_name)
            VALUES (:inst)
            ON CONFLICT (instance_name) DO NOTHING;
        """), {"inst": inst})

    # dim_metric
    for metric, unit in df[['metric_name', 'original_unit']].drop_duplicates().values:
        conn.execute(text("""
            INSERT INTO dim_metric (metric_name, original_unit)
            VALUES (:metric, :unit)
            ON CONFLICT (metric_name) DO NOTHING;
        """), {"metric": metric, "unit": unit})

    # dim_component
    for comp, ctype in df[['component_name', 'component_type']].drop_duplicates().values:
        conn.execute(text("""
            INSERT INTO dim_component (component_name, component_type)
            VALUES (:comp, :ctype)
            ON CONFLICT (component_name, component_type) DO NOTHING;
        """), {"comp": comp, "ctype": ctype})

    # dim_date
    for ts in df['timestamp_utc'].drop_duplicates():
        ts2 = pd.to_datetime(ts)
        conn.execute(text("""
            INSERT INTO dim_date (timestamp_utc, year, month, day, hour, minute, second)
            VALUES (:ts, :y, :m, :d, :h, :min, :s)
            ON CONFLICT (timestamp_utc) DO NOTHING;
        """), {
            "ts": ts2, "y": ts2.year, "m": ts2.month, "d": ts2.day,
            "h": ts2.hour, "min": ts2.minute, "s": ts2.second
        })

print("- Dimensions insérées")

#  CHARGER LES IDS
dim_instance = pd.read_sql("SELECT * FROM dim_instance;", engine)
dim_metric = pd.read_sql("SELECT * FROM dim_metric;", engine)
dim_component = pd.read_sql("SELECT * FROM dim_component;", engine)
dim_date = pd.read_sql("SELECT * FROM dim_date;", engine)

dim_date['timestamp_utc'] = pd.to_datetime(dim_date['timestamp_utc'], utc=True)

# Merge
df_facts = df.merge(dim_instance, left_on='instance', right_on='instance_name')
df_facts = df_facts.merge(dim_metric, on='metric_name')
df_facts = df_facts.merge(dim_component, on=['component_name', 'component_type'])
df_facts = df_facts.merge(dim_date, on='timestamp_utc')

#  INSERT FACTS
with engine.begin() as conn:
    for _, row in df_facts.iterrows():
        conn.execute(text("""
            INSERT INTO fact_metrics (date_id, instance_id, metric_id, component_id, value)
            VALUES (:d, :i, :m, :c, :v)
            ON CONFLICT (date_id, instance_id, metric_id, component_id) DO NOTHING;
        """), {
            "d": row['date_id'], "i": row['instance_id'],
            "m": row['metric_id'], "c": row['component_id'],
            "v": row['value']
        })

print("- Faits insérés avec succès")

#  EXPORT CSV 
fact_df = pd.read_sql("""
SELECT f.fact_id, d.timestamp_utc, i.instance_name, m.metric_name, m.original_unit,
       c.component_name, c.component_type, f.value
FROM fact_metrics f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_instance i ON f.instance_id = i.instance_id
JOIN dim_metric m ON f.metric_id = m.metric_id
JOIN dim_component c ON f.component_id = c.component_id
ORDER BY d.timestamp_utc;
""", engine)

fact_df.to_csv("metrics_star_schema.csv", index=False)
print("- Export fichier csv")