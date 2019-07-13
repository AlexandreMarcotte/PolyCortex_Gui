# --My packages--
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget
from pyqtgraph.dockarea import Dock
from V2.utils.colors import *


class PlotDock(Dock):
    def __init__(self, plot=ScrollPlotWidget, curve_color=pen_colors):
        super().__init__(name='', hideTitle=True)
        self.plot = plot(curve_color=curve_color)

        self.addWidget(self.plot, 0, 1, 4, 5)
        self.setStyleSheet('background-color:rgba(0, 0, 0, 255);')

