# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.inner_docks.eeg_settings_dock import EegSettingsDock
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.inner_docks.eeg_plots_dock import EegPlotsDock


class EegDock(InnerDock):
    def __init__(self):
        super().__init__(
                name='EEG', toggle_btn=False, add_dock_area=True,
                set_scroll=True, hide_title=False)

        self.settings_dock = EegSettingsDock(self.layout)
        self.plots_dock = EegPlotsDock()

        self.inner_docks = [self.settings_dock, self.plots_dock]
        self.add_all_dock_to_dock_area()

    def add_all_dock_to_dock_area(self):
        for inner_dock in self.inner_docks:
            self.dock_area.addDock(inner_dock.dock)

