import numpy as np

class ADSR:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.params = {
            'attack': 0.1,   # seconds
            'decay': 0.3,    # seconds
            'sustain': 0.7,  # level (0.0-1.0)
            'release': 0.5   # seconds
        }
        
    def generate_envelope(self, duration):
        total_samples = int(duration * self.sample_rate)
        envelope = np.zeros(total_samples)
        
        # Attack phase
        attack_samples = int(self.params['attack'] * self.sample_rate)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay phase
        decay_samples = int(self.params['decay'] * self.sample_rate)
        decay_start = attack_samples
        decay_end = decay_start + decay_samples
        envelope[decay_start:decay_end] = np.linspace(1, self.params['sustain'], decay_samples)
        
        # Sustain phase (until release)
        sustain_level = self.params['sustain']
        release_start = decay_end
        envelope[release_start:-1] = sustain_level
        
        # Release phase
        release_samples = int(self.params['release'] * self.sample_rate)
        release_end = min(total_samples, release_start + release_samples)
        envelope[release_start:release_end] = np.linspace(sustain_level, 0, release_end - release_start)
        
        return envelope