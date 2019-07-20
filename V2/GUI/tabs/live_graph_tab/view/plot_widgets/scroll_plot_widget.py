import pyqtgraph as pg
import re
# --My Packages--
from .live_plot import LivePlot
from V2.utils.colors import Color


class ScrollPlotWidget(pg.PlotWidget, LivePlot):
    def __init__(self, curve_color=Color.pen_colors):
        """Signals: list of signal to plot in this scroll plot"""
        super().__init__()

        self.curve_color = curve_color

        self.signals = [0]
        self.curves = []
        # Curve
        # self.curves = self._init_curves()
        self._init_plot_appearance()

    def _init_plot_appearance(self):
        self.plotItem.showGrid(x=True, y=True, alpha=0.2)
        self.plotItem.setLabel(axis='left', units='v')
        self.plotItem.hideAxis('bottom')
        self.setBackground(Color.dark_grey)

    def connect_timers(self, t_interval=0):
        self.timer = self.init_timer()
        self.timer.start(t_interval)

    def connect_signals(self, signals):
        self.signals = signals
        self.curves = self._init_curves(signals)
        # Start the timer at the connection

    def _init_curves(self, signals):
        curves = []
        for i, signal in enumerate(signals):
            curve = self.plot(signal)
            # TODO: ALEXM: Or do a modulo over the list of colors
            try:
                color = self.curve_color[i]
            except:
                color = Color.pen_colors[i]
            curve.setPen(color)
            curves.append(curve)
        return curves

    def _update(self):
        for curve, signal in zip(self.curves, self.signals):
            curve.setData(signal)

    def scale_axis(self, txt, axis='y'):
        try:
            if txt == 'Auto':
                self.enableAutoRange()
            else:
                r = int(re.search(r'\d+', txt).group())
                if axis == 'y':
                    self.setYRange(-r, r)
                elif axis == 'x':
                    self.setXRange(0, r)
        except AttributeError as e:
            print("Invalide value")

    def set_log_mode(self, is_log):
        self.setLogMode(y=eval(is_log))


