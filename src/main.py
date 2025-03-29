import sys
import sounddevice as sounddevice
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget
from gui.elektron_menu import ElektronMenu
from gui.performance_grid import PerformanceGrid
from gui.transport_controls import TransportControls
from sampler.waveform_editor import WaveformEditor
from sampler.engine import SamplerEngine
from mixer.channel_strip import ChannelStrip
from src.sampler.midi_mapper import MidiMapper

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sampler = SamplerEngine()
        self.midi_mapper = MidiMapper()
        self.midi_mapper.start_listening_thread()
        self._setup_ui()
        
    def _setup_ui(self):
        # Central waveform editor
        self.waveform_editor = WaveformEditor()
        self.setCentralWidget(self.waveform_editor)
        
        # Dock widgets
        self.mixer_dock = QDockWidget("Mixer", self)
        self.mixer_dock.setWidget(ChannelStrip())
        self.addDockWidget(2, self.mixer_dock)
        
        self.grid = PerformanceGrid()
        grid_widget = QWidget()
        grid_widget.setLayout(self.grid)
        self.addDockWidget(1, QDockWidget("Performance Grid", self)).setWidget(grid_widget)
        
        # Elektron-style menu
        self.menu = ElektronMenu()
        self.addDockWidget(1, QDockWidget("Controls", self)).setWidget(self.menu)
        
        # Transport controls
        self.transport_controls = TransportControls()
        self.addDockWidget(1, QDockWidget("Transport", self)).setWidget(self.transport_controls)

    def __del__(self):
        self.midi_mapper.stop_listening()

class AudioEngine:
    def __init__(self, sr=48000, buffer_size=512):
        self.sr = sr
        self.buffer_size = buffer_size
        self.mix_buffer = np.zeros((buffer_size, 2), dtype=np.float32)
        self.lock = Lock()
        self.fx_rack = Pedalboard()
        
        self.stream = sounddevice.OutputStream(
            samplerate=sr,
            blocksize=buffer_size,
            callback=self._callback,
            dtype='float32'
        )

    def _callback(self, outdata, frames, time, status):
        with self.lock:
            processed = self.fx_rack.process(self.mix_buffer, self.sr)
            outdata[:] = processed
            self.mix_buffer.fill(0)

    def add_audio(self, audio):
        with self.lock:
            end = min(len(audio), self.buffer_size)
            self.mix_buffer[:end] += audio[:end]

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 1280, 720)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
