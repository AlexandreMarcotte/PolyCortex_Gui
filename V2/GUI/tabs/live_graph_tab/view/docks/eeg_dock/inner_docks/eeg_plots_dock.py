from typing import List
# --My packages--
from V2.utils.my_dock import MyDock
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget


class EegPlotsDock(MyDock):
    def __init__(self):
        super().__init__('eeg_plots_dock', hide_title=False)
        self._init_plots()

    def _init_plots(self):
        self.plot_docks: List[PlotDock] = []
        for ch in range(8):
            plot_dock = PlotDock(ch=ch, plot=ScrollPlotWidget())
            self.plot_docks.append(plot_dock)
            self.dock_area.addDock(plot_dock)

