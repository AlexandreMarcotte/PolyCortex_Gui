from pyqtgraph.dockarea import *
# --My packages--
from pyqtgraph.dockarea.Dock import DockLabel
from ..live_graph_tab.update_style_patch import update_style_patched


class PlotDockWidget(Dock):
    def __init__(self, name, plot):
        DockLabel.updateStyle = update_style_patched
        super().__init__(name)
        self.addWidget(plot)
