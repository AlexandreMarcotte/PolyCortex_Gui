# -- My packages --
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from .inner_docks.spectrogram_settings_dock import SpectrogramSettingsDock
from .inner_docks.spectrogram_plot_dock import SpectrogramPlotDock


class SpectrogramDock(InnerDock):
    def __init__(self, name='Spectrogram'):
        super().__init__(
            name=name, toggle_btn=False, add_dock_area=True, set_scroll=True,
            hide_title=False)

        self._add_all_dock_to_dock_area()

    def _add_all_dock_to_dock_area(self):
        self._add_settings_dock()
        self._add_plot()

    def _add_settings_dock(self):
        self.settings_dock = SpectrogramSettingsDock(self.inner_layout)
        self.dock_area.addDock(self.settings_dock)

    def _add_plot(self):
        self.plot_dock = SpectrogramPlotDock()
        self.dock_area.addDock(self.plot_dock)

    # TODO: ALEXM: connect inside instead
    # def connect_start_btn(self):
    #     self.settings_dock.start_btn.clicked.connect(
    #         self.plot_dock.start())





