import numpy as np
import pyqtgraph as pg

class WaveGraph:
    def __init__(self, wave_plot, one_ch_deque):
        self.wave_plot = wave_plot
        self.one_ch_deque = one_ch_deque

        self.x = np.arange(10)
        self.y = np.sin(self.x)
        self.bg1 = pg.BarGraphItem(x=self.x, height=self.y, width=1, brush='b')
        self.wave_plot.addItem(self.bg1)

    def update_wave_plotting(self):
        # Remove All item from the graph
        self.wave_plot.clear()
        self.y = np.random.random(10)
        self.bg1 = pg.BarGraphItem(x=self.x, height=self.y, width=1, brush='b')
        self.wave_plot.addItem(self.bg1)
