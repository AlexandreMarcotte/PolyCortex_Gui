from pyqtgraph.dockarea import *
# --My packages--
from V2.GUI.scroll_plot_widget import ScrollPlotWidget
from pyqtgraph.dockarea.Dock import DockLabel
from V2.general_func.update_style_patch import update_style_patched


class PlotDockWidget(Dock):
    def __init__(self, name, signals=()):
        DockLabel.updateStyle = update_style_patched
        super().__init__(name)
        self.addWidget(ScrollPlotWidget(signals))