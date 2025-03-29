import configparser
from pathlib import Path

class AudioMIDISettings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = Path.home() / '.config' / 'tuxtrax' / 'settings.ini'
        self._load_defaults()
        self.load()
        
    def _load_defaults(self):
        self.config['Audio'] = {
            'device': 'default',
            'samplerate': '48000',
            'buffersize': '256',
            'latency_comp': '0'
        }
        self.config['MIDI'] = {
            'inputs': '',
            'sync': '0'
        }
        
    def save(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            self.config.write(f)
    
    def load(self):
        if self.config_path.exists():
            self.config.read(self.config_path)
    
    @property
    def buffer_size(self):
        return self.config['Audio'].getint('buffersize')