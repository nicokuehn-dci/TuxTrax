import librosa
from pydub import AudioSegment

def load_audio_file(file_path):
    """Load audio file using librosa"""
    y, sr = librosa.load(file_path, sr=None, mono=True)
    return y, sr

def convert_format(input_path, output_format='wav'):
    """Convert audio files using pydub"""
    sound = AudioSegment.from_file(input_path)
    output_path = input_path.rsplit('.', 1)[0] + f'.{output_format}'
    sound.export(output_path, format=output_format)
    return output_path

def load_audio_into_memory(file_path):
    """Load audio file into memory using librosa"""
    audio_data, sr = librosa.load(file_path, sr=None, mono=False)
    return audio_data, sr

def time_stretch_audio(audio_data, rate):
    """Time-stretch audio using librosa"""
    return librosa.effects.time_stretch(audio_data, rate)

def quantize_to_bpm(audio_data, sr, bpm):
    """Quantize audio to the given BPM using librosa"""
    hop_length = int(60 / bpm * sr)
    return librosa.effects.time_stretch(audio_data, hop_length)
