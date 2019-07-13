import pyqtgraph as pg
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.live_plot import LivePlot


class TimePlot(pg.PlotWidget, LivePlot):
    def __init__(self, curve_color=('w')):
        super().__init__()

        self.curr_time = [0, 10]

        self._init_plot_appearance()
        self.timer = self.init_timer()

    def _init_plot_appearance(self):
        self.plotItem.hideAxis('left')
        self.plotItem.hideAxis('bottom')
        self.plotItem.showAxis('top')

    def _update(self):
        self._increase_time()

    def _increase_time(self):
        self.setXRange(self.curr_time[0], self.curr_time[-1])
