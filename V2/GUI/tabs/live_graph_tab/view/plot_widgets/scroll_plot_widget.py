# -- General Packages --
import pyqtgraph as pg
import re
from pyqtgraph import LinearRegionItem
from typing import List
# --My Packages--
from .live_plot import LivePlot
from V2.utils.colors import Color
from V2.general_settings import GeneralSettings


class ScrollPlotWidget(pg.PlotWidget, LivePlot):
    def __init__(self, curve_color=Color.pen_colors):
        """Signals: list of signal to plot in this scroll plot"""
        super().__init__()

        self.curve_color = curve_color

        self.regions: List[LinearRegionItem] = []
        self.signals = [0]
        self.curves = []
        self.events_pos = None
        # Curve
        # self.curves = self._init_curves()
        self._init_plot_appearance()

    def _init_plot_appearance(self):
        self.plotItem.showGrid(x=True, y=True, alpha=0.2)
        self.plotItem.setLabel(axis='left', units='v')
        self.plotItem.hideAxis('bottom')
        self.setBackground(Color.dark_grey)
        for _ in range(8):
            self.spawn_following_region()

    def connect_timers(self, t_interval=0):
        self.timer = self.init_timer()
        self.timer.start(t_interval)

    def connect_signals(self, signals):
        """Connect in the connectors"""
        self.signals = signals
        self.curves = self._init_curves(signals)
        # Start the timer at the connection

    def connect_events_pos(self, events_pos):
        """Connect in the connectors"""
        self.events_pos = events_pos

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

    def change_curves_color(self, color_btn):
        self.curves[0].setPen(color_btn.color())

    def _update(self):
        for curve, signal in zip(self.curves, self.signals):
            curve.setData(signal)
        self._update_region()

    def _update_region(self):
        if self.events_pos:
            for no, region in enumerate(self.regions):
                if no < len(self.events_pos):
                    pos = GeneralSettings.QUEUE_LEN - self.events_pos[no]
                    left_pos = pos
                    right_pos = pos + GeneralSettings.REGION_WIDTH
                    # Make sure the event region doesn't get out of the plot
                    # view on the right and left side
                    if right_pos > GeneralSettings.QUEUE_LEN:
                        right_pos = GeneralSettings.QUEUE_LEN
                    elif left_pos < 0:
                        left_pos = 0
                    region.setRegion([left_pos, right_pos])
                # Remove region if not used any more
                else:
                    left_bound, right_bound = region.getRegion()
                    if left_bound != 0:
                        region.setRegion([0, 0])

    def scale_axis(self, txt, axis='y', symetric=False):
        try:
            if txt == 'Auto':
                self.enableAutoRange()
            else:
                r = int(re.search(r'\d+', txt).group())
                if axis == 'y':
                    if symetric:
                        self.setYRange(-r, r)
                    else:
                        self.setYRange(0, r)
                elif axis == 'x':
                    self.setXRange(0, r)
        except AttributeError as e:
            print("Invalide value")

    def set_log_mode(self, is_log):
        self.setLogMode(y=eval(is_log))

    def spawn_following_region(self):
        queue_len = GeneralSettings.QUEUE_LEN
        region = LinearRegionItem(values=[queue_len, queue_len])
        self.addItem(region)
        self.regions.append(region)


