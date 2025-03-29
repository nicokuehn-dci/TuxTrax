import numpy as np

class BusRouter:
    def __init__(self, num_buses=4):
        self.buses = {
            'main': {'level': 1.0, 'sources': []},
            'reverb': {'level': 0.3, 'sources': []},
            'delay': {'level': 0.2, 'sources': []},
            'sidechain': {'level': 0.0, 'sources': []}
        }
        self.tracks = []
        self._setup_multitrack()
        
    def add_to_bus(self, bus_name, audio_data):
        if bus_name in self.buses:
            self.buses[bus_name]['sources'].append(audio_data)
            
    def mix_bus(self, bus_name):
        if bus_name not in self.buses:
            return np.zeros(1024)
            
        mixed = np.sum(self.buses[bus_name]['sources'], axis=0)
        return mixed * self.buses[bus_name]['level']
    
    def clear_buses(self):
        for bus in self.buses.values():
            bus['sources'].clear()
            
    def _setup_multitrack(self):
        for i in range(8):  # Example: 8 tracks
            track = {
                'name': f'Track {i+1}',
                'audio_data': [],
                'midi_data': []
            }
            self.tracks.append(track)
            
    def add_audio_to_track(self, track_index, audio_data):
        if 0 <= track_index < len(self.tracks):
            self.tracks[track_index]['audio_data'].append(audio_data)

    def add_midi_to_track(self, track_index, midi_data):
        if 0 <= track_index < len(self.tracks):
            self.tracks[track_index]['midi_data'].append(midi_data)
