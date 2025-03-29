from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class ChannelStrip(QWidget):
    volume_changed = pyqtSignal(float)  # 0.0-1.0
    pan_changed = pyqtSignal(float)     # -1.0 (left) to 1.0 (right)

    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        # Volume Slider
        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(75)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        layout.addWidget(QLabel("Volume"))
        layout.addWidget(self.volume_slider)
        
        # Pan Control
        self.pan_slider = QSlider(Qt.Vertical)
        self.pan_slider.setRange(-50, 50)
        self.pan_slider.setValue(0)
        self.pan_slider.valueChanged.connect(self._on_pan_changed)
        layout.addWidget(QLabel("Pan"))
        layout.addWidget(self.pan_slider)
        
        self.setLayout(layout)

    def _on_volume_changed(self, value):
        self.volume_changed.emit(value / 100.0)

    def _on_pan_changed(self, value):
        self.pan_changed.emit(value / 50.0)
