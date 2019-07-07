import pyqtgraph as pg
import re
# --My Packages--
from .live_plot import LivePlot


class ScrollPlotWidget(pg.PlotWidget, LivePlot):
    def __init__(self):
        """Signals: list of signal to plot in this scroll plot"""
        super().__init__()
        self.signals = []
        # Curve
        self.curves = self._init_curves()

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


