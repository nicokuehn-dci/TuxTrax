import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

class WaveformEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)
        self.plot_widget.setYRange(-1, 1)
        self.plot_widget.showGrid(x=True, y=True)
        self.start_marker = pg.InfiniteLine(angle=90, movable=True, pen='r')
        self.end_marker = pg.InfiniteLine(angle=90, movable=True, pen='g')
        self.loop_start_marker = pg.InfiniteLine(angle=90, movable=True, pen='b')
        self.loop_end_marker = pg.InfiniteLine(angle=90, movable=True, pen='y')
        self.plot_widget.addItem(self.start_marker)
        self.plot_widget.addItem(self.end_marker)
        self.plot_widget.addItem(self.loop_start_marker)
        self.plot_widget.addItem(self.loop_end_marker)

    def set_waveform(self, data):
        self.plot_widget.plot(data, clear=True)
        self.start_marker.setPos(0)
        self.end_marker.setPos(len(data))
        self.loop_start_marker.setPos(0)
        self.loop_end_marker.setPos(len(data))

    def get_markers(self):
        return {
            'start': self.start_marker.value(),
            'end': self.end_marker.value(),
            'loop_start': self.loop_start_marker.value(),
            'loop_end': self.loop_end_marker.value()
        }
