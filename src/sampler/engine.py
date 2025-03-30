import numpy as np
import librosa
from .midi_mapper import MidiMapper
from ..utils.audio_utils import load_audio_file
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SamplerEngine:
    """Core sampler engine handling audio loading and playback.
    
    Attributes:
        samples (dict): Stores loaded samples with metadata
        loops (dict): Stores loaded loops with metadata
        midi_mapper (MidiMapper): Handles MIDI input mapping
        current_bpm (int): Current beats per minute for playback
        playback_mode (str): Mode of playback (e.g., "one-shot")
        tracks (list): List of tracks for multi-track recording
        automation_lanes (list): List of automation lanes for parameters
    """
    
    def __init__(self):
        self.samples = {}
        self.loops = {}
        self.midi_mapper = MidiMapper()
        self.current_bpm = 120
        self.playback_mode = "one-shot"
        self.tracks = []
        self.automation_lanes = []
        self._setup_multitrack()
        self._setup_automation_lanes()

    def load_sample(self, file_path, name, is_loop=False):
        """Load an audio file into the sampler.
        
        Args:
            file_path (str): Path to the audio file
            name (str): Name to assign to the loaded sample
            is_loop (bool): Whether the sample is a loop
            
        Returns:
            bool: True if the sample was loaded successfully
        """
        try:
            audio_data, sr = load_audio_file(file_path)
            bpm = self._detect_bpm(audio_data, sr)
            quantized_audio = self._quantize_to_bpm(audio_data, sr, bpm)
            sample_data = {
                'data': quantized_audio,
                'sr': sr,
                'length': len(quantized_audio),
                'key': self._detect_key(quantized_audio, sr),
                'bpm': bpm
            }
            if is_loop:
                self.loops[name] = sample_data
            else:
                self.samples[name] = sample_data
            return True
        except Exception as e:
            logger.error(f"Error loading sample {name} from {file_path}: {e}")
            return False

    def load_loop(self, file_path, name):
        """Load a loop into the sampler.
        
        Args:
            file_path (str): Path to the loop file
            name (str): Name to assign to the loaded loop
            
        Returns:
            bool: True if the loop was loaded successfully
        """
        return self.load_sample(file_path, name, is_loop=True)

    def _detect_key(self, audio_data, sr):
        """Detect the musical key of the audio sample.
        
        Args:
            audio_data (np.ndarray): Audio data array
            sr (int): Sample rate of the audio data
            
        Returns:
            str: Detected key of the audio sample
        """
        try:
            chroma = librosa.feature.chroma_cqt(y=audio_data, sr=sr)
            return librosa.core.key_to_notes(np.argmax(chroma.mean(axis=1)))[0]
        except Exception as e:
            logger.error(f"Error detecting key: {e}")
            return None

    def _detect_bpm(self, audio_data, sr):
        """Detect the BPM of the audio sample.
        
        Args:
            audio_data (np.ndarray): Audio data array
            sr (int): Sample rate of the audio data
            
        Returns:
            float: Detected BPM of the audio sample
        """
        try:
            tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)
            return tempo
        except Exception as e:
            logger.error(f"Error detecting BPM: {e}")
            return None

    def _quantize_to_bpm(self, audio_data, sr, bpm):
        """Quantize the audio sample to the given BPM.
        
        Args:
            audio_data (np.ndarray): Audio data array
            sr (int): Sample rate of the audio data
            bpm (float): BPM to quantize the audio to
            
        Returns:
            np.ndarray: Quantized audio data
        """
        try:
            hop_length = int(60 / bpm * sr)
            return librosa.effects.time_stretch(audio_data, hop_length)
        except Exception as e:
            logger.error(f"Error quantizing to BPM: {e}")
            return audio_data

    def map_to_midi(self, sample_name, midi_note):
        """Map a sample to a MIDI note.
        
        Args:
            sample_name (str): Name of the sample to map
            midi_note (int): MIDI note number to map the sample to
        """
        try:
            if sample_name in self.samples:
                self.midi_mapper.map_note_to_sample(midi_note, sample_name)
        except Exception as e:
            logger.error(f"Error mapping sample {sample_name} to MIDI note {midi_note}: {e}")

    def process_audio(self, sample_name, start, end, is_loop=False):
        """Process audio for playback.
        
        Args:
            sample_name (str): Name of the sample to process
            start (int): Start index for playback
            end (int): End index for playback
            is_loop (bool): Whether the sample is a loop
            
        Returns:
            np.ndarray: Processed audio data
        """
        try:
            if is_loop:
                sample_dict = self.loops
            else:
                sample_dict = self.samples

            if sample_name not in sample_dict:
                return np.array([])
            
            sample = sample_dict[sample_name]
            audio_data = sample['data'][start:end]
            
            # Apply any additional processing here (e.g., effects, envelopes)
            
            return audio_data
        except Exception as e:
            logger.error(f"Error processing audio for sample {sample_name}: {e}")
            return np.array([])

    def _setup_multitrack(self):
        try:
            for i in range(8):  # Example: 8 tracks
                track = {
                    'name': f'Track {i+1}',
                    'audio_data': [],
                    'midi_data': []
                }
                self.tracks.append(track)
        except Exception as e:
            logger.error(f"Error setting up multitrack: {e}")

    def _setup_automation_lanes(self):
        try:
            for i in range(8):  # Example: 8 automation lanes
                lane = {
                    'name': f'Automation Lane {i+1}',
                    'data': []
                }
                self.automation_lanes.append(lane)
        except Exception as e:
            logger.error(f"Error setting up automation lanes: {e}")

    def add_audio_to_track(self, track_index, audio_data):
        """Add audio data to a specific track.
        
        Args:
            track_index (int): Index of the track to add audio to
            audio_data (np.ndarray): Audio data to add
        """
        try:
            if 0 <= track_index < len(self.tracks):
                self.tracks[track_index]['audio_data'].append(audio_data)
        except Exception as e:
            logger.error(f"Error adding audio to track {track_index}: {e}")

    def add_midi_to_track(self, track_index, midi_data):
        """Add MIDI data to a specific track.
        
        Args:
            track_index (int): Index of the track to add MIDI to
            midi_data (list): MIDI data to add
        """
        try:
            if 0 <= track_index < len(self.tracks):
                self.tracks[track_index]['midi_data'].append(midi_data)
        except Exception as e:
            logger.error(f"Error adding MIDI to track {track_index}: {e}")

    def add_automation_data(self, lane_index, automation_data):
        """Add automation data to a specific lane.
        
        Args:
            lane_index (int): Index of the lane to add automation to
            automation_data (list): Automation data to add
        """
        try:
            if 0 <= lane_index < len(self.automation_lanes):
                self.automation_lanes[lane_index]['data'].append(automation_data)
        except Exception as e:
            logger.error(f"Error adding automation data to lane {lane_index}: {e}")

    def fetch_high_quality_output(self, sample_name):
        """Fetch high-quality output for a sample.
        
        Args:
            sample_name (str): Name of the sample to fetch output for
            
        Returns:
            np.ndarray: High-quality audio data
        """
        try:
            if sample_name not in self.samples:
                return np.array([])
            
            sample = self.samples[sample_name]
            audio_data = sample['data']
            
            # Apply any additional processing here (e.g., effects, mastering)
            
            return audio_data
        except Exception as e:
            logger.error(f"Error fetching high-quality output for sample {sample_name}: {e}")
            return np.array([])
