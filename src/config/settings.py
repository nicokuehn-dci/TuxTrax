class AudioMIDISettings:
    def __init__(self, sample_rate=44100, buffer_size=512, midi_device="default"):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.midi_device = midi_device

    def load_settings(self, settings_dict):
        self.sample_rate = settings_dict.get("sample_rate", self.sample_rate)
        self.buffer_size = settings_dict.get("buffer_size", self.buffer_size)
        self.midi_device = settings_dict.get("midi_device", self.midi_device)

    def save_settings(self):
        return {
            "sample_rate": self.sample_rate,
            "buffer_size": self.buffer_size,
            "midi_device": self.midi_device
        }
