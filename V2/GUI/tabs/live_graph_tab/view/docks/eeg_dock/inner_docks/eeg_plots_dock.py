from typing import List
# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock


class EegPlotsDock(InnerDock):
    def __init__(self, size=(1, 10)):
        # DockLabel.updateStyle = update_style_patched
        super().__init__(
                name='eeg_plots_dock', size=size, toggle_btn=False,
                add_dock_area=True, set_scroll=True)
        self._init_plots()

    def _init_plots(self):
        self.plot_docks: List[PlotDock] = []
        for ch in range(8):
            plot_dock = PlotDock(ch=ch)
            self.plot_docks.append(plot_dock)
            self.dock_area.addDock(plot_dock)

