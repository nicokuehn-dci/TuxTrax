import mido
from mido import Message
import threading

class MidiMapper:
    def __init__(self):
        self.mapping = {}  # {midi_note: sample_path}
        self.listener_thread = None
        self.stop_event = threading.Event()
        
    def map_note_to_sample(self, note, sample_path):
        self.mapping[note] = sample_path
        
    def start_listening_thread(self):
        self.listener_thread = threading.Thread(target=self.start_listening)
        self.listener_thread.start()
        
    def start_listening(self):
        with mido.open_input(callback=self.callback) as inport:
            self.stop_event.wait()
            
    def stop_listening(self):
        if self.listener_thread and self.listener_thread.is_alive():
            self.stop_event.set()
            self.listener_thread.join()
            
    def callback(self, msg):
        if msg.type == 'note_on':
            self.trigger_sample(msg.note)

    def trigger_sample(self, note):
        if note in self.mapping:
            # Add sample triggering logic
            print(f"Triggering sample: {self.mapping[note]}")
