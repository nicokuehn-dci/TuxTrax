import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget
from gui.elektron_menu import ElektronMenu
from gui.performance_grid import PerformanceGrid
from gui.transport_controls import TransportControls
from sampler.waveform_editor import WaveformEditor
from sampler.engine import SamplerEngine
from mixer.channel_strip import ChannelStrip
from src.sampler.midi_mapper import MidiWorker, MidiManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sampler = SamplerEngine()
        self.midi_manager = MidiManager()
        self.midi_manager.start()
        self._setup_ui()
        self._connect_midi_signals()
        self.tracks = []
        self.automation_lanes = []
        self._setup_multitrack()
        self._setup_automation_lanes()
        
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

    def _connect_midi_signals(self):
        self.midi_manager.worker.note_on.connect(self.handle_note_on)
        self.midi_manager.worker.cc_changed.connect(self.handle_cc_changed)

    def handle_note_on(self, note, velocity):
        print(f"Note on: {note} with velocity {velocity}")

    def handle_cc_changed(self, cc_number, value):
        print(f"CC changed: {cc_number} with value {value}")

    def _setup_multitrack(self):
        for i in range(8):  # Example: 8 tracks
            track = {
                'name': f'Track {i+1}',
                'audio_data': [],
                'midi_data': []
            }
            self.tracks.append(track)

    def _setup_automation_lanes(self):
        for i in range(8):  # Example: 8 automation lanes
            lane = {
                'name': f'Automation Lane {i+1}',
                'data': []
            }
            self.automation_lanes.append(lane)

    def __del__(self):
        self.midi_manager.stop()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 1280, 720)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
