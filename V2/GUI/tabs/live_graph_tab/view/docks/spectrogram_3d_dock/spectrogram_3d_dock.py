# -- My packages --
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from .inner_docks.spectrogram_3d_settings import Spectrogram3dSettings
from .inner_docks.spectrogram_3d_plot import Spectrogram3dPlot


class Spectrogram3dDock(InnerDock):
    def __init__(self, name='Spectrogram 3D'):
        super().__init__(
            name=name, toggle_btn=False, add_dock_area=True, set_scroll=True,
            hide_title=False)

        self._add_all_dock_to_dock_area()

    def _add_all_dock_to_dock_area(self):
        self._add_settings_dock()
        self._add_plot()

    def _add_settings_dock(self):
        self.settings_dock = Spectrogram3dSettings(self.inner_layout)
        self.dock_area.addDock(self.settings_dock)

    def _add_plot(self):
        self.plot = Spectrogram3dPlot()
        self.dock_area.addDock(self.plot)
