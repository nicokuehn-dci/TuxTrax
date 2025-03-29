from PyQt5.QtCore import QObject, pyqtSignal, QThread
import mido

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
    
    def start(self):
        self.thread.start()
    
    def stop(self):
        self.worker.running = False
        self.thread.quit()