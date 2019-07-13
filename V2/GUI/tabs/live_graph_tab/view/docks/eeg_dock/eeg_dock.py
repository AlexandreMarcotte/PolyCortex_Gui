from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from .inner_docks.eeg_settings_dock import EegSettingsDock
from .inner_docks.eeg_plots_dock import EegPlotsDock
from .inner_docks.saving_dock import SavingDock
from .inner_docks.banner_dock import BannerDock
from .inner_docks.write_to_hardware_dock import WriteHardwareDock
from .inner_docks.pins_settings_dock import PinsSettingsDock


class EegDock(InnerDock):
    def __init__(self, name='EEG', external_layout=None):
        super().__init__(
            name=name, toggle_btn=False, add_dock_area=True, set_scroll=True,
            hide_title=False, margin=(7, 0, 0, 0))

        self.external_layout = external_layout
        self._add_all_dock_to_dock_area()

    def _add_all_dock_to_dock_area(self):
        self._add_settings_dock()
        self._add_plot_dock()
        self._add_saving_dock()
        self._add_banner_dock()
        self._add_write_hardware_dock()

    def _add_settings_dock(self):
        self.settings_dock = EegSettingsDock(self.inner_layout)
        self.dock_area.addDock(self.settings_dock)

    def _add_plot_dock(self):
        pins_settings_dock = PinsSettingsDock(external_layout=self)
        self.plot_dock = EegPlotsDock(
            pins_settings_dock=pins_settings_dock)
        self.dock_area.addDock(self.plot_dock)

    def _add_saving_dock(self):
        self.saving_dock = SavingDock(external_layout=self.inner_layout)
        self.dock_area.addDock(self.saving_dock, 'top', self.plot_dock)

    def _add_banner_dock(self):
        self.banner_dock = BannerDock(external_layout=self.inner_layout)
        self.dock_area.addDock(self.banner_dock, 'top', self.plot_dock)
        self.banner_dock.hide()

    def _add_write_hardware_dock(self):
        self.write_hardware_dock = WriteHardwareDock(
            external_layout=self.inner_layout)
        self.dock_area.addDock(self.write_hardware_dock, 'top', self.plot_dock)
        self.write_hardware_dock.hide()

