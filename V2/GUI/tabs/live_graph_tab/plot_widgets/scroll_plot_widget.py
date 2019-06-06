import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
# --My Packages--
from .live_plot import LivePlot


class ScrollPlotWidget(pg.PlotWidget, LivePlot):
    def __init__(self, signals=()):
        super().__init__()
        self.signals = signals
        # Curve
        self.curves = self.init_curves(signals)
        # Timer
        self.timer = self.init_timer()
        self.timer.start(10)

    def init_curves(self, signals):
        curves = []
        for signal in signals:
            curves.append(self.plot(signal))
        return curves

    def update(self):
        for i, signal in enumerate(self.signals):
            self.curves[i].setData(signal)


