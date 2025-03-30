from PyQt5.QtCore import QObject, pyqtSignal, QThread
import mido
import pipewire as pw
import alsa_midi as am

class MidiWorker(QObject):
    note_on = pyqtSignal(int, float)  # (note, velocity 0.0-1.0)
    control_change = pyqtSignal(int, float)  # (cc_num, 0.0-1.0)

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
                        self.control_change.emit(msg.control, msg.value/127)

class MidiManager:
    def __init__(self):
        self.thread = QThread()
        self.worker = MidiWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        
        # Initialize PipeWire MIDI
        pw.init(None, None)
        self.context = pw.Context()
        self.core = self.context.connect()
        self.midi_stream = pw.MidiStream(self.core, "TuxTrax-MIDI", pw.MIDI_DIRECTION_INPUT | pw.MIDI_DIRECTION_OUTPUT, None)
        self.midi_stream.connect(pw.ID_ANY, 0)
        
        # Initialize ALSA MIDI fallback
        self.alsa_midi_in = None
        self.alsa_midi_out = None
        try:
            self.alsa_midi_in = am.Input("hw:1", am.NONBLOCK)
            self.alsa_midi_out = am.Output("hw:1", am.NONBLOCK)
        except Exception as e:
            print(f"ALSA MIDI initialization failed: {e}")

    def start(self):
        self.thread.start()
    
    def stop(self):
        self.worker.running = False
        self.thread.quit()
