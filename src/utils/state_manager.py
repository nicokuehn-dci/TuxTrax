import json
import pickle
from pathlib import Path

class ProjectManager:
    def save_project(self, path, sampler_state, mixer_state):
        project_data = {
            'samples': sampler_state.samples,
            'midi_mapping': sampler_state.midi_mapper.mapping,
            'mixer_presets': mixer_state.get_presets()
        }
        
        with open(Path(path) / 'project.tux', 'wb') as f:
            pickle.dump(project_data, f)
            
    def load_project(self, path):
        with open(Path(path) / 'project.tux', 'rb') as f:
            return pickle.load(f)

    def save_state(self, path, state):
        with open(Path(path) / 'state.json', 'w') as f:
            json.dump(state, f)

    def load_state(self, path):
        with open(Path(path) / 'state.json', 'r') as f:
            return json.load(f)
