class BaseConfig:
    # Shared defaults
    RESULTS_DIR = "results"
    PROM_URL = "http://localhost:9090/api/v1/query"
    CSV_SINK = "results/prometheus_metrics_log.csv"
    CLEAN_DATA = "results/nifi_metrics_propre.csv" 
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