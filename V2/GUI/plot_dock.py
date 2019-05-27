from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
# --My packages--
from V2.GUI.scroll_plot import ScrollPlot


class PlotDock(QDockWidget):
    def __init__(self, name, signals=()):
        super().__init__(name)
        self.setStyleSheet(
            'QDockWidget::title { background-color:rgba(60, 160, 210, 1); }')
        self.scroll_plot = self.add_plot(signals)

    def add_plot(self, signals):
        scroll_plot = ScrollPlot(signals)
        self.setWidget(scroll_plot)
        return scroll_plot
