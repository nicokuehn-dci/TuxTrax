from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QDial, QLabel

class ElektronMenu(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout()
        
        # Encoder Simulation
        self.encoders = []
        for i in range(4):
            encoder = QDial()
            encoder.setRange(0, 127)
            encoder.setNotchesVisible(True)
            label = QLabel(f"Param {i+1}")
            
            col = QVBoxLayout()
            col.addWidget(encoder)
            col.addWidget(label)
            layout.addLayout(col)
            self.encoders.append((encoder, label))
            
        self.setLayout(layout)