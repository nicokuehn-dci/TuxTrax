import mido
from mido import Message
import threading
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class MidiWorker(QObject):
    note_on = pyqtSignal(int, int)  # (note, velocity)
    cc_changed = pyqtSignal(int, float)  # (cc_number, 0.0-1.0)

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        self.running = True
        try:
            with mido.open_input() as port:
                while self.running:
                    for msg in port.iter_pending():
                        if msg.type == 'note_on':
                            self.note_on.emit(msg.note, msg.velocity/127)
                        elif msg.type == 'control_change':
                            self.cc_changed.emit(msg.control, msg.value/127)
        except Exception as e:
            logger.error(f"Error in MIDI worker run loop: {e}")

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
            try:
                # Add sample triggering logic
                print(f"Triggering sample: {self.mapping[note]} with velocity {velocity}")
            except Exception as e:
                logger.error(f"Error triggering sample for note {note}: {e}")

    def auto_quantize_midi(self, midi_data, bpm):
        """Auto quantize MIDI data to the given BPM.
        
        Args:
            midi_data (list): List of MIDI messages
            bpm (float): BPM to quantize the MIDI to
            
        Returns:
            list: Quantized MIDI messages
        """
        quantized_midi = []
        tick_duration = 60 / bpm / 24  # Assuming 24 ticks per quarter note
        for msg in midi_data:
            if msg.type in ['note_on', 'note_off']:
                quantized_time = round(msg.time / tick_duration) * tick_duration
                quantized_msg = msg.copy(time=quantized_time)
                quantized_midi.append(quantized_msg)
            else:
                quantized_midi.append(msg)
        return quantized_midi
