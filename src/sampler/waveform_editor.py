from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np

class WaveformEditor(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setBackground('#1a1a1a')
        self.plotItem.hideAxis('bottom')
        self.plotItem.hideAxis('left')
        self.waveform = self.plot([0], pen='#00ff00')
        
        # Waveform markers
        self.start_marker = pg.InfiniteLine(pos=0, angle=90, pen='#ff0000')
        self.end_marker = pg.InfiniteLine(pos=1, angle=90, pen='#ff0000')
        self.loop_region = pg.LinearRegionItem([0, 1], brush='#ffffff20')
        
        self.addItem(self.start_marker)
        self.addItem(self.end_marker)
        self.addItem(self.loop_region)

    def load_audio(self, data):
        self.waveform.setData(self.decimate_data(data))

    def decimate_data(self, data, factor=10):
        return data[::factor]
