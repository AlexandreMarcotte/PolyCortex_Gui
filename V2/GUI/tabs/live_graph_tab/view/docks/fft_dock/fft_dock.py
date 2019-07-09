# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.inner_docks.fft_settings_dock import FftSettingsDock
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock


class FftDock(InnerDock):
    def __init__(self):
        super().__init__(
            name='FFT', toggle_btn=False, add_dock_area=True,
            set_scroll=True, hide_title=False)

        self.settings_dock = FftSettingsDock(self.layout)
        self.plot_dock = PlotDock(add_btn=False)

        self.inner_docks = [self.settings_dock, self.plot_dock]
        self.add_all_dock_to_dock_area()

    def add_all_dock_to_dock_area(self):
        for inner_dock in self.inner_docks:
            # TODO: ALEXM: Try to remove this construct
            try:
                self.dock_area.addDock(inner_dock.dock)
            except AttributeError:
                self.dock_area.addDock(inner_dock)

