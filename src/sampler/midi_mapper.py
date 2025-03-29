import mido
from mido import Message

class MidiMapper:
    def __init__(self):
        self.mapping = {}  # {midi_note: sample_path}
        
    def map_note_to_sample(self, note, sample_path):
        self.mapping[note] = sample_path
        
    def start_listening(self):
        with mido.open_input() as inport:
            for msg in inport:
                if msg.type == 'note_on':
                    self.trigger_sample(msg.note)

    def trigger_sample(self, note):
        if note in self.mapping:
            # Add sample triggering logic
            print(f"Triggering sample: {self.mapping[note]}")