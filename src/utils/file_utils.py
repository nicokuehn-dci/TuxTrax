import os
import yaml
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

def load_config(config_path="config/default.yaml"):
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return {}

def get_sample_library_paths():
    try:
        config = load_config()
        default_path = Path.home() / "TuxTrax_Samples"
        return [
            default_path,
            *config.get('library_paths', [])
        ]
    except Exception as e:
        logging.error(f"Failed to get sample library paths: {e}")
        return []

def create_project_folder(project_name):
    try:
        base_path = Path.home() / "TuxTrax_Projects"
        project_path = base_path / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        return str(project_path)
    except Exception as e:
        logging.error(f"Failed to create project folder: {e}")
        return ""
