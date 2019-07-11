from pyqtgraph.dockarea import Dock
# --My packages--
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget


class PlotDock(Dock):
    def __init__(self, plot=ScrollPlotWidget, curve_color='b'):
        super().__init__(name='', hideTitle=True)
        self.plot = plot(curve_color=curve_color)

        self.addWidget(self.plot, 0, 1, 4, 9)

