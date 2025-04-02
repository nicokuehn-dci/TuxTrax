import os
import yaml
from pathlib import Path
import json
import logging

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

def save_pattern_to_file(pattern, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(pattern, f)
    except Exception as e:
        logging.error(f"Error saving pattern to file {file_path}: {e}")

def load_pattern_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading pattern from file {file_path}: {e}")
        return None
