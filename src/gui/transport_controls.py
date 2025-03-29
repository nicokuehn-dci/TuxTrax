from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import pyqtSignal

class TransportControls(QWidget):
    playClicked = pyqtSignal()
    stopClicked = pyqtSignal()
    recordClicked = pyqtSignal()
    automationChanged = pyqtSignal(int, float)  # (parameter index, value)
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Transport buttons
        transport_layout = QHBoxLayout()
        self.play_btn = QPushButton("▶")
        self.play_btn.setStyleSheet("font-size: 18px;")
        self.play_btn.clicked.connect(self.playClicked.emit)
        
        self.stop_btn = QPushButton("◼")
        self.stop_btn.setStyleSheet("font-size: 18px;")
        self.stop_btn.clicked.connect(self.stopClicked.emit)
        
        self.record_btn = QPushButton("⏺")
        self.record_btn.setStyleSheet("font-size: 18px; color: red;")
        self.record_btn.clicked.connect(self.recordClicked.emit)
        
        transport_layout.addWidget(self.stop_btn)
        transport_layout.addWidget(self.play_btn)
        transport_layout.addWidget(self.record_btn)
        
        # Automation lanes
        automation_layout = QVBoxLayout()
        self.automation_sliders = []
        for i in range(8):  # Example: 8 automation lanes
            slider = QSlider()
            slider.setOrientation(Qt.Horizontal)
            slider.setRange(0, 127)
            slider.valueChanged.connect(lambda value, idx=i: self.automationChanged.emit(idx, value / 127.0))
            label = QLabel(f"Param {i+1}")
            automation_layout.addWidget(label)
            automation_layout.addWidget(slider)
            self.automation_sliders.append(slider)
        
        layout.addLayout(transport_layout)
        layout.addLayout(automation_layout)
        self.setLayout(layout)
