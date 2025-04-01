from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class PerformanceGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.record_button = QPushButton("Record")
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.record_button)
        self.setLayout(self.layout)

        self.play_button.clicked.connect(self.parent().play)
        self.stop_button.clicked.connect(self.parent().stop)
        self.record_button.clicked.connect(self.parent().record)
