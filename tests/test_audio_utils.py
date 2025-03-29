import sys
import os
import pytest
import numpy as np
import soundfile as sf

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.audio_utils import load_audio_file

def test_load_audio_file(tmp_path):
    # Create test WAV file
    test_file = tmp_path / "test.wav"
    rate = 44100
    data = np.random.rand(rate * 2)  # 2-second noise
    sf.write(str(test_file), data, rate)
    
    # Test loading
    loaded_data, sr = load_audio_file(str(test_file))
    assert sr == rate
    assert len(loaded_data) == len(data)
    assert np.allclose(loaded_data, data, atol=0.01)