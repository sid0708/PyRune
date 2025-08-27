# src/modules/utils.py
import yaml
import os

def load_yaml_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_env_var(name, default=None):
    return os.getenv(name, default)
