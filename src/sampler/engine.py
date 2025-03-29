import numpy as np
from .midi_mapper import MidiMapper
from ..utils.audio_utils import load_audio_file

class SamplerEngine:
    def __init__(self):
        self.samples = {}
        self.midi_mapper = MidiMapper()
        self.current_bpm = 120
        self.playback_mode = "one-shot"

    def load_sample(self, file_path, name):
        audio_data, sr = load_audio_file(file_path)
        self.samples[name] = {
            'data': audio_data,
            'sr': sr,
            'length': len(audio_data),
            'key': self._detect_key(audio_data, sr)
        }
        return True

    def _detect_key(self, audio_data, sr):
        chroma = librosa.feature.chroma_cqt(y=audio_data, sr=sr)
        return librosa.core.key_to_notes(np.argmax(chroma.mean(axis=1)))[0]

    def map_to_midi(self, sample_name, midi_note):
        if sample_name in self.samples:
            self.midi_mapper.map_note_to_sample(midi_note, sample_name)