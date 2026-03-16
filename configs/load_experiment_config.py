from pathlib import Path

import yaml


def load_experiment_config():

    config_path = Path(__file__).parent / "experiment_config.yaml"

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config

config = load_experiment_config()
print(config)