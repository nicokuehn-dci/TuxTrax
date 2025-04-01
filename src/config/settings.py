class AudioMIDISettings:
    def __init__(self, sample_rate=44100, buffer_size=512, midi_device="default", magenta_studio_path="", aiva_path="", chatgpt4_music_plugins_path=""):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.midi_device = midi_device
        self.magenta_studio_path = magenta_studio_path
        self.aiva_path = aiva_path
        self.chatgpt4_music_plugins_path = chatgpt4_music_plugins_path

    def load_settings(self, settings_dict):
        self.sample_rate = settings_dict.get("sample_rate", self.sample_rate)
        self.buffer_size = settings_dict.get("buffer_size", self.buffer_size)
        self.midi_device = settings_dict.get("midi_device", self.midi_device)
        self.magenta_studio_path = settings_dict.get("magenta_studio_path", self.magenta_studio_path)
        self.aiva_path = settings_dict.get("aiva_path", self.aiva_path)
        self.chatgpt4_music_plugins_path = settings_dict.get("chatgpt4_music_plugins_path", self.chatgpt4_music_plugins_path)

    def save_settings(self):
        return {
            "sample_rate": self.sample_rate,
            "buffer_size": self.buffer_size,
            "midi_device": self.midi_device,
            "magenta_studio_path": self.magenta_studio_path,
            "aiva_path": self.aiva_path,
            "chatgpt4_music_plugins_path": self.chatgpt4_music_plugins_path
        }
