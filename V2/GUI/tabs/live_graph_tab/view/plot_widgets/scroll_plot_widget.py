import pyqtgraph as pg
import re
# --My Packages--
from .live_plot import LivePlot
from V2.utils.colors import *


class ScrollPlotWidget(pg.PlotWidget, LivePlot):
    def __init__(self):
        """Signals: list of signal to plot in this scroll plot"""
        super().__init__()
        self.signals = []
        # Curve
        self._init_plot_appearance()
        self.curves = self._init_curves()

    def _init_plot_appearance(self):
        self.plotItem.showGrid(x=True, y=True, alpha=0.2)
        self.plotItem.setLabel(axis='left', units='v')
        self.plotItem.hideAxis('bottom')
        self.setBackground(dark_grey)
        # self.setYRange(-3000, 3000)

    def _init_curves(self):
        curves = []
        # for signal in signals:
        for ch in range(8):
            curves.append(self.plot())
        return curves

    def connect_signals(self, signals):
        self.signals = signals

    def update(self):
        for i, signal in enumerate(self.signals):
            self.curves[i].setData(signal)

    def scale_y_axis(self, txt):
        try:
            if txt == 'Auto':
                self.enableAutoRange()
            else:
                r = int(re.search(r'\d+', txt).group())
                self.setYRange(-r, r)
        except AttributeError as e:
            print("Invalide value")


