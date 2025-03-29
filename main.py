import sys
import sounddevice as sounddevice
import numpy as np
from threading import Thread, Lock
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget
from gui.elektron_menu import ElektronMenu
from gui.performance_grid import PerformanceGrid
from gui.transport_controls import TransportControls
from sampler.waveform_editor import WaveformEditor
from sampler.engine import SamplerEngine
from mixer.channel_strip import ChannelStrip
from src.sampler.midi_mapper import MidiMapper
from pedalboard import Pedalboard
from src.audio.midi_handler import MidiManager
from src.audio.engine import AudioEngine
from src.config.settings import AudioMIDISettings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self.init_background_tasks()

    def init_background_tasks(self):
        self.audio_engine = AudioEngine()
        self.audio_thread = Thread(target=self.audio_engine.start)
        self.audio_thread.start()
        self.sampler = SamplerEngine()
        self.midi_mapper = MidiMapper()
        self.midi_mapper.start_listening_thread()

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
        self.audio_engine.stop()
        self.audio_thread.join()

    def closeEvent(self, event):
        self.midi_mapper.stop_listening()
        self.audio_engine.stop()
        self.audio_thread.join()
        event.accept()

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
        if status:
            print(f"Stream status: {status}")
        try:
            with self.lock:
                processed = self.fx_rack.process(self.mix_buffer, self.sr)
                outdata[:] = processed
                self.mix_buffer.fill(0)
        except Exception as e:
            print(f"Error in audio callback: {e}")
            outdata.fill(0)

    def add_audio(self, audio):
        with self.lock:
            for i in range(0, len(audio), self.buffer_size):
                chunk = audio[i:i + self.buffer_size]
                end = min(len(chunk), self.buffer_size)
                self.mix_buffer[:end] += chunk[:end]

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
