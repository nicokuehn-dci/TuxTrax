from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class TransportControls(QWidget):
    playClicked = pyqtSignal()
    stopClicked = pyqtSignal()
    recordClicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        
        self.play_btn = QPushButton("▶")
        self.play_btn.setStyleSheet("font-size: 18px;")
        self.play_btn.clicked.connect(self.playClicked.emit)
        
        self.stop_btn = QPushButton("◼")
        self.stop_btn.setStyleSheet("font-size: 18px;")
        self.stop_btn.clicked.connect(self.stopClicked.emit)
        
        self.record_btn = QPushButton("⏺")
        self.record_btn.setStyleSheet("font-size: 18px; color: red;")
        self.record_btn.clicked.connect(self.recordClicked.emit)
        
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.play_btn)
        layout.addWidget(self.record_btn)
        self.setLayout(layout)
