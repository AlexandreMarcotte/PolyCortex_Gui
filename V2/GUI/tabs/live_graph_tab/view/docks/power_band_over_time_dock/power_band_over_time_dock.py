# -- My packages --
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from .inner_docks.power_band_over_time_settings import PowerBandOverTimeSettings
from .inner_docks.power_band_over_time_plot import PowerBandOverTimePlot
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock
from V2.utils.colors import Color
# TEST
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.inner_docks.plot.fft_plot import FftPlot


class PowerBandOverTimeDock(InnerDock):
    def __init__(self, name='Power band over time'):
        super().__init__(
            name=name, toggle_btn=False, add_dock_area=True, set_scroll=True,
            hide_title=False)

        self._add_all_dock_to_dock_area()

    def _add_all_dock_to_dock_area(self):
        self._add_settings_dock()
        self._add_plot()

    def _add_settings_dock(self):
        self.settings_dock = PowerBandOverTimeSettings(self.inner_layout)
        self.dock_area.addDock(self.settings_dock)

    def _add_plot(self):
        self.plot = PlotDock(plot=PowerBandOverTimePlot(
            curve_color=Color.pen_colors))
        self.dock_area.addDock(self.plot)
