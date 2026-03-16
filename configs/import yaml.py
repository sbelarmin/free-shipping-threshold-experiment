import yaml


def load_experiment_config(path="configs/experiment_config.yaml"):

    with open(path, "r") as f:
        config = yaml.safe_load(f)

    return config


config = load_experiment_config()

print(config["experiment"]["arms"])