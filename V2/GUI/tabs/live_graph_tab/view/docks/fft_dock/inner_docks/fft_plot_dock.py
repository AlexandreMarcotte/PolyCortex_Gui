from typing import List
# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock


class FftPlotsDock(InnerDock):
    def __init__(self, size=(1, 10)):
        super().__init__(
                name='fft_plots_dock', size=size, toggle_btn=False,
                add_dock_area=True, set_scroll=True)
        self._init_plots()

    def _init_plots(self):
        plot_dock = PlotDock(add_btn=False)

