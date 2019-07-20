# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.inner_docks.filter_dock import FilterDock
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.inner_docks.fft_settings_dock import FftSettingsDock
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.inner_docks.plot.fft_plot import FftPlot
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock
from V2.utils.colors import Color


class FftDock(InnerDock):
    def __init__(self, name='FFT', margin=(0, 0, 0, 0), external_layout=None):
        super().__init__(
            name=name, toggle_btn=False, add_dock_area=True, set_scroll=True,
            hide_title=False, margin=margin)

        self.external_layout = external_layout
        self._add_all_dock_to_dock_area()

    def _add_all_dock_to_dock_area(self):
        self._add_settings_dock()
        self._add_plot()
        self._add_filter_dock()

    def _add_filter_dock(self):
        # Filter dock
        self.filter_dock = FilterDock(external_layout=self.inner_layout)
        self.dock_area.addDock(self.filter_dock, 'right', self.plot_dock)
        self.filter_dock.hide()

    def _add_settings_dock(self):
        self.settings_dock = FftSettingsDock(self.inner_layout)
        self.dock_area.addDock(self.settings_dock)

    def _add_plot(self):
        self.plot_dock = PlotDock(plot=FftPlot(curve_color=Color.pen_colors))
        self.dock_area.addDock(self.plot_dock)


