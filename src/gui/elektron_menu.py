from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QDial, QLabel
from PyQt5.QtCore import pyqtSignal

class ElektronMenu(QWidget):
    encoder_changed = pyqtSignal(int, int)  # Encoder index and value

    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout()
        
        # Encoder Simulation
        self.encoders = []
        for i in range(4):
            encoder = QDial()
            encoder.setRange(0, 127)
            encoder.setNotchesVisible(True)
            encoder.valueChanged.connect(lambda value, idx=i: self.encoder_changed.emit(idx, value))
            label = QLabel(f"Param {i+1}")
            
            col = QVBoxLayout()
            col.addWidget(encoder)
            col.addWidget(label)
            layout.addLayout(col)
            self.encoders.append((encoder, label))
            
        self.setLayout(layout)
