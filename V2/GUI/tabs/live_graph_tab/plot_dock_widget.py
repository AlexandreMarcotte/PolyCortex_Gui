from pyqtgraph.dockarea import *
# --My packages--
from V2.GUI.scroll_plot_widget import ScrollPlotWidget
from V2.GUI.scroll_plot_widget import GraphicLayoutWidget
from pyqtgraph.dockarea.Dock import DockLabel
from V2.GUI.tabs.live_graph_tab.update_style_patch import update_style_patched


class PlotDockWidget(Dock):   # TODO: ALEX: Faire un heritage a la place de faire un dispatch comme ça
    def __init__(self, name, signals=(), plot_type='1D'):
        DockLabel.updateStyle = update_style_patched
        super().__init__(name)
        if plot_type == '1D':
            self.addWidget(ScrollPlotWidget(signals))
        elif plot_type == '2D':
            self.addWidget(GraphicLayoutWidget(signals))