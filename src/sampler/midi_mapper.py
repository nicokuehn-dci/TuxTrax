import mido
from mido import Message
from PyQt5.QtCore import QThread, pyqtSignal, QObject

class MidiMapper(QObject):
    note_triggered = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.mapping = {}  # {midi_note: sample_path}
        self.listener_thread = None

    def map_note_to_sample(self, note, sample_path):
        self.mapping[note] = sample_path

    def start_listening(self):
        if self.listener_thread is None:
            self.listener_thread = MidiListener(self.mapping)
            self.listener_thread.note_triggered.connect(self.trigger_sample)
            self.listener_thread.start()

    def trigger_sample(self, note):
        if note in self.mapping:
            # Add sample triggering logic
            print(f"Triggering sample: {self.mapping[note]}")

class MidiListener(QThread):
    note_triggered = pyqtSignal(int)

    def __init__(self, mapping):
        super().__init__()
        self.mapping = mapping

    def run(self):
        with mido.open_input() as inport:
            for msg in inport:
                if msg.type == 'note_on':
                    self.note_triggered.emit(msg.note)
