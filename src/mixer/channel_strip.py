from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class ChannelStrip(QWidget):
    volume_changed = pyqtSignal(int)
    pan_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        # Volume Slider
        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(75)
        self.volume_slider.valueChanged.connect(self.volume_changed.emit)
        layout.addWidget(QLabel("Volume"))
        layout.addWidget(self.volume_slider)
        
        # Pan Control
        self.pan_slider = QSlider(Qt.Vertical)
        self.pan_slider.setRange(-50, 50)
        self.pan_slider.setValue(0)
        self.pan_slider.valueChanged.connect(self.pan_changed.emit)
        layout.addWidget(QLabel("Pan"))
        layout.addWidget(self.pan_slider)
        
        self.setLayout(layout)
