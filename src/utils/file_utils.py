import os
import yaml
from pathlib import Path

def load_config(config_path="config/default.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_sample_library_paths():
    config = load_config()
    default_path = Path.home() / "TuxTrax_Samples"
    return [
        default_path,
        *config.get('library_paths', [])
    ]

def create_project_folder(project_name):
    base_path = Path.home() / "TuxTrax_Projects"
    project_path = base_path / project_name
    project_path.mkdir(parents=True, exist_ok=True)
    return str(project_path)