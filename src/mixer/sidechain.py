from pedalboard import Compressor, Gain
import numpy as np

class SidechainEngine:
    def __init__(self):
        self.threshold = -24
        self.ratio = 4.0
        self.attack = 10.0
        self.release = 100.0
        self.makeup_gain = 6.0
        self.comp = Compressor(
            threshold_db=self.threshold,
            ratio=self.ratio,
            attack_ms=self.attack,
            release_ms=self.release
        )
        self.makeup_gain_processor = Gain(gain_db=self.makeup_gain)

    def set_parameters(self, threshold=None, ratio=None, attack=None, release=None, makeup_gain=None):
        if threshold is not None:
            self.threshold = threshold
        if ratio is not None:
            self.ratio = ratio
        if attack is not None:
            self.attack = attack
        if release is not None:
            self.release = release
        if makeup_gain is not None:
            self.makeup_gain = makeup_gain

        self.comp = Compressor(
            threshold_db=self.threshold,
            ratio=self.ratio,
            attack_ms=self.attack,
            release_ms=self.release
        )
        self.makeup_gain_processor = Gain(gain_db=self.makeup_gain)

    def process(self, main_audio, trigger_audio, sr):
        # Convert trigger audio to envelope
        envelope = np.abs(trigger_audio)
        envelope = np.convolve(envelope, np.ones(1024)/1024, mode='same')
        
        # Apply compression based on envelope
        compressed = self.comp(main_audio, sr)
        return self.makeup_gain_processor(compressed * envelope, sr)
