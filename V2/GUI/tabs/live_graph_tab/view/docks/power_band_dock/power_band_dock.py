# -- My packages --
from V2.GUI.tabs.inner_dock import InnerDock
from .inner_docks.power_band_settings import PowerBandSettings
from .inner_docks.power_band_plot import PowerBandPlot


class PowerBandDock(InnerDock):
    def __init__(self, name='Power band'):
        super().__init__(
            name=name, toggle_btn=False, add_dock_area=True, set_scroll=True,
            hide_title=False)

        self._add_all_dock_to_dock_area()

    def _add_all_dock_to_dock_area(self):
        self._add_settings_dock()
        self._add_plot()

    def _add_settings_dock(self):
        self.settings_dock = PowerBandSettings(self.inner_layout)
        self.dock_area.addDock(self.settings_dock)

    def _add_plot(self):
        self.plot = PowerBandPlot()
        self.dock_area.addDock(self.plot)

