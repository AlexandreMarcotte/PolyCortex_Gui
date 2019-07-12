from typing import List
# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from .eeg_plot_dock import EegPlotDock
from .time_plot import TimePlot
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock


class EegPlotsDock(InnerDock):
    def __init__(self, size=(1, 10)):
        super().__init__(
            name='eeg_plots_dock', size=size, toggle_btn=False,
            add_dock_area=True, set_scroll=True,
            back_ground_color=False)

        self._init_plots()

    def _init_plots(self):
        self.plot_docks: List[EegPlotDock] = []
        for ch in range(9):
            if ch == 8:
                self.time_dock = PlotDock(plot=TimePlot, curve_color=('k'))
                self.dock_area.addDock(self.time_dock)
            else:
                plot_dock = EegPlotDock(ch)
                self.plot_docks.append(plot_dock)
                self.dock_area.addDock(plot_dock)



