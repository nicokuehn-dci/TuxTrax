import mido
from mido import Message
import threading
from PyQt5.QtCore import QObject, pyqtSignal, QThread

class MidiWorker(QObject):
    note_on = pyqtSignal(int, int)  # (note, velocity)
    cc_changed = pyqtSignal(int, float)  # (cc_number, 0.0-1.0)

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        self.running = True
        with mido.open_input() as port:
            while self.running:
                for msg in port.iter_pending():
                    if msg.type == 'note_on':
                        self.note_on.emit(msg.note, msg.velocity/127)
                    elif msg.type == 'control_change':
                        self.cc_changed.emit(msg.control, msg.value/127)

class MidiMapper:
    def __init__(self):
        self.mapping = {}  # {midi_note: sample_path}
        self.worker = MidiWorker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.note_on.connect(self.trigger_sample)
        
    def map_note_to_sample(self, note, sample_path):
        self.mapping[note] = sample_path
        
    def start_listening_thread(self):
        self.thread.started.connect(self.worker.run)
        self.thread.start()
        
    def stop_listening(self):
        self.worker.running = False
        self.thread.quit()
        self.thread.wait()
            
    def trigger_sample(self, note, velocity):
        if note in self.mapping:
            # Add sample triggering logic
            print(f"Triggering sample: {self.mapping[note]} with velocity {velocity}")
