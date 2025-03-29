import numpy as np
from .midi_mapper import MidiMapper
from ..utils.audio_utils import load_audio_file

class SamplerEngine:
    """Core sampler engine handling audio loading and playback.
    
    Attributes:
        samples (dict): Stores loaded samples with metadata
        midi_mapper (MidiMapper): Handles MIDI input mapping
        current_bpm (int): Current beats per minute for playback
        playback_mode (str): Mode of playback (e.g., "one-shot")
    """
    
    def __init__(self):
        self.samples = {}
        self.midi_mapper = MidiMapper()
        self.current_bpm = 120
        self.playback_mode = "one-shot"

    def load_sample(self, file_path, name):
        """Load an audio file into the sampler.
        
        Args:
            file_path (str): Path to the audio file
            name (str): Name to assign to the loaded sample
            
        Returns:
            bool: True if the sample was loaded successfully
        """
        audio_data, sr = load_audio_file(file_path)
        self.samples[name] = {
            'data': audio_data,
            'sr': sr,
            'length': len(audio_data),
            'key': self._detect_key(audio_data, sr)
        }
        return True

    def _detect_key(self, audio_data, sr):
        """Detect the musical key of the audio sample.
        
        Args:
            audio_data (np.ndarray): Audio data array
            sr (int): Sample rate of the audio data
            
        Returns:
            str: Detected key of the audio sample
        """
        chroma = librosa.feature.chroma_cqt(y=audio_data, sr=sr)
        return librosa.core.key_to_notes(np.argmax(chroma.mean(axis=1)))[0]

    def map_to_midi(self, sample_name, midi_note):
        """Map a sample to a MIDI note.
        
        Args:
            sample_name (str): Name of the sample to map
            midi_note (int): MIDI note number to map the sample to
        """
        if sample_name in self.samples:
            self.midi_mapper.map_note_to_sample(midi_note, sample_name)
