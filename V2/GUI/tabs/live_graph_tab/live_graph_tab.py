from pyqtgraph.dockarea import *
from V2.GUI.tabs.live_graph_tab.plot_dock_widget import PlotDockWidget
from V2.pipeline.pipeline import Pipeline
from PyQt5.QtWidgets import *


class LiveGraphTab(QWidget):
    def __init__(self):
        super().__init__()
        # Start pipeline
        self.pipeline = Pipeline()

        self.area = DockArea()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.area)
        # Init docks
        self.plot_dock = self.init_plot_dock()
        self.filter_signal_dock = self.init_filter_signal_dock()

    def init_plot_dock(self):
        plot_dock = PlotDockWidget(
                'Input Signal', signals=[self.pipeline.signal_collector.input])
        self.area.addDock(plot_dock)
        return plot_dock

    def init_filter_signal_dock(self):
        filter_signal_dock = PlotDockWidget(
                'Filtered Signal', signals=[self.pipeline.filter_stage.output])
        self.area.addDock(filter_signal_dock)
        return filter_signal_dock


