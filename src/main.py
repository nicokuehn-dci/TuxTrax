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
from src.audio.engine import AudioEngine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sampler = SamplerEngine()
        self.midi_mapper = MidiMapper()
        self.midi_mapper.start_listening_thread()
        self._setup_ui()
        try:
            self.audio_engine = AudioEngine()
            self.audio_thread = Thread(target=self.audio_engine.start)
            self.audio_thread.start()
        except Exception as e:
            print(f"Error initializing AudioEngine: {e}")
            sys.exit(1)
        
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

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 1280, 720)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
