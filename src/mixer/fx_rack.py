from pedalboard import Pedalboard, Compressor, Reverb, Gain, Chorus, Delay, Distortion

class FXEngine:
    def __init__(self):
        self.inserts = Pedalboard([
            Compressor(threshold=-20, ratio=4),
            Gain(gain_db=6),
            Distortion(drive_db=20)
        ])
        
        self.sends = Pedalboard([
            Reverb(room_size=0.7, damping=0.5),
            Chorus(),
            Delay()
        ])

    def process_audio(self, audio, sample_rate):
        processed = self.inserts(audio, sample_rate)
        send_effect = self.sends(processed, sample_rate)
        return processed + send_effect * 0.3  # Dry/Wet mix
