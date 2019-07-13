from typing import List
# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from .eeg_plot_dock import EegPlotDock
from .time_plot import TimePlot
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock


class EegPlotsDock(InnerDock):
    def __init__(self, size=(1, 10), pins_settings_dock=None):
        super().__init__(
            name='eeg_plots_dock', size=size, toggle_btn=False,
            add_dock_area=True, set_scroll=True)

        self.pins_settings_dock = pins_settings_dock
        self.dock_area.addDock(self.pins_settings_dock)

        self._init_plots()

        self.pins_settings_dock.hide()

    def _init_plots(self):
        self.plot_docks: List[EegPlotDock] = []
        # Time plot
        self.time_dock = PlotDock(plot=TimePlot, curve_color=('k'))
        self.dock_area.addDock(
            self.time_dock)
        for ch in range(8):
            # EEG plots
            plot_dock = EegPlotDock(ch)
            self.plot_docks.append(plot_dock)
            if ch == 0:
                self.dock_area.addDock(plot_dock, 'right', self.pins_settings_dock)
            else:
                self.dock_area.addDock(plot_dock, 'bottom', self.plot_docks[0])



