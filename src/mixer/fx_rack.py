from pedalboard import Pedalboard, Compressor, Reverb, Gain

class FXEngine:
    def __init__(self):
        self.inserts = Pedalboard([
            Compressor(threshold=-20, ratio=4),
            Gain(gain_db=6)
        ])
        
        self.sends = Pedalboard([
            Reverb(room_size=0.7, damping=0.5)
        ])
        self.active_effects = []

    def process_audio(self, audio, sample_rate):
        processed = self.inserts(audio, sample_rate)
        send_effect = self.sends(processed, sample_rate)
        return processed + send_effect * 0.3  # Dry/Wet mix

    def add_effect(self, effect):
        self.active_effects.append(effect)

    def remove_effect(self, effect):
        if effect in self.active_effects:
            self.active_effects.remove(effect)

    def apply_effects(self, audio, sample_rate):
        for effect in self.active_effects:
            audio = effect(audio, sample_rate)
        return audio
