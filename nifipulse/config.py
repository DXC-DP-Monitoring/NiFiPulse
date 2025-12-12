import os
from urllib.parse import quote_plus

class BaseConfig:
    # Shared defaults
    PROM_URL = "http://localhost:9090/api/v1/query"
    RESULTS_DIR = os.getenv("RESULTS_DIR", "results")
    CSV_SINK = os.getenv("CSV_SINK", os.path.join(RESULTS_DIR, "prometheus_metrics_log.csv"))
    CLEAN_DATA = os.getenv("CLEAN_DATA", os.path.join(RESULTS_DIR, "nifi_metrics_clean.csv"))
    FACT_METRICS = os.getenv("FACT_METRICS", os.path.join(RESULTS_DIR, "fact_metrics_export.csv"))
    # Build DSN from env (override PGHOST to 'postgres' when running inside Docker)
    PW = quote_plus(os.getenv('PGPASSWORD', 'postgres'))
    PG_DSN = os.getenv(
        "PG_DSN",
        "postgresql+psycopg2://"
        f"{os.getenv('PGUSER','postgres')}:{PW}@"
        f"{os.getenv('PGHOST','localhost')}:{os.getenv('PGPORT','5432')}/"
        f"{os.getenv('PGDATABASE','metrics_db')}"
    )
class DevConfig(BaseConfig):
    pass


class StagedConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    pass


# Default environment
env = ProdConfig

ENV_MAP = {"dev": DevConfig, "staged": StagedConfig, "prod": ProdConfig}

def set_env(env_name):
    global env
    try:
        env = ENV_MAP[env_name]
    except KeyError:
        raise ValueError(f"Unknown environment: {env_name}")

def set_env_from_branch(branch_name: str):
    """
    Map Git branch to environment: main->prod, staging->staged, dev->dev
    """
    mapping = {"main": "prod", "staging": "staged", "dev": "dev"}
    set_env(mapping.get(branch_name, "prod"))

def auto_set_env():
    name = os.getenv("NIFIPULSE_ENV")
    if name:
        set_env(name)
        return
    branch = os.getenv("GITHUB_REF_NAME") or (os.getenv("GITHUB_REF","").split("/")[-1] or "main")
    set_env_from_branch(branch)

if os.getenv("NIFIPULSE_AUTO_ENV") == "1":
    auto_set_env()