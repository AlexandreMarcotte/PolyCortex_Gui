import pyqtgraph as pg
import re
# --My Packages--
from .live_plot import LivePlot
from V2.utils.colors import *


class ScrollPlotWidget(pg.PlotWidget, LivePlot):
    def __init__(self, curve_color=('w')):
        """Signals: list of signal to plot in this scroll plot"""
        super().__init__()

        self.curve_color = curve_color

        self.signals = []
        self.curves = []
        # Curve
        # self.curves = self._init_curves()

    def _init_plot_appearance(self):
        self.plotItem.showGrid(x=True, y=True, alpha=0.2)
        self.plotItem.setLabel(axis='left', units='v')
        self.plotItem.hideAxis('bottom')
        self.setBackground(dark_grey)

    def _init_curves(self, signals):
        curves = []
        for color, signal in zip(self.curve_color, signals):
            curve = self.plot(signal)
            curve.setPen(color)
            curves.append(curve)
        return curves

    def connect_signals(self, signals, t_interval=0):
        self._init_plot_appearance()
        self.signals = signals
        self.curves = self._init_curves(signals)
        # Start the timer at the connection
        self.timer = self.init_timer()
        self.timer.start(t_interval)

    def _update(self):
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


