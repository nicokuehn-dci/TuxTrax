import json
import pickle
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ProjectManager:
    def save_project(self, path, sampler_state, mixer_state):
        try:
            project_data = {
                'samples': sampler_state.samples,
                'midi_mapping': sampler_state.midi_mapper.mapping,
                'mixer_presets': mixer_state.get_presets()
            }
            
            with open(Path(path) / 'project.tux', 'wb') as f:
                pickle.dump(project_data, f)
        except Exception as e:
            logger.error(f"Error saving project: {e}")
            raise

    def load_project(self, path):
        try:
            with open(Path(path) / 'project.tux', 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Error loading project: {e}")
            raise

    def save_state(self, path, state):
        try:
            with open(Path(path) / 'state.json', 'w') as f:
                json.dump(state, f)
        except Exception as e:
            logger.error(f"Error saving state: {e}")
            raise

    def load_state(self, path):
        try:
            with open(Path(path) / 'state.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            raise
