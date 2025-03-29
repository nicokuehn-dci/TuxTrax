from PyQt5.QtWidgets import QGridLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class PerformanceGrid(QGridLayout):
    pad_triggered = pyqtSignal(int)  # Emits pad index (0-15)

    def __init__(self):
        super().__init__()
        self.pads = []
        self._create_pads()

    def _create_pads(self):
        for i in range(4):
            for j in range(4):
                btn = QPushButton()
                btn.setStyleSheet("""
                    QPushButton {
                        background: #333;
                        border-radius: 5px;
                        min-width: 60px;
                        min-height: 60px;
                    }
                    QPushButton:pressed {
                        background: #666;
                    }
                """)
                btn.clicked.connect(lambda _, idx=i*4+j: self.pad_triggered.emit(idx))
                self.addWidget(btn, i, j)
                self.pads.append(btn)
