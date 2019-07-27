from V2.GUI.tabs.inner_dock import InnerDock
from .inner_docks.eeg_settings_dock import EegSettingsDock
from .inner_docks.eeg_plots_dock import EegPlotsDock
from .inner_docks.saving_dock import SavingDock
from .inner_docks.banner_dock import BannerDock
from .inner_docks.write_to_hardware_dock import WriteHardwareDock
from V2.utils.rotated_button import RotatedButton
from V2.general_settings import GeneralSettings


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
        self._add_pins_settings_btn()

    def _add_settings_dock(self):
        self.settings_dock = EegSettingsDock(self.inner_layout)
        self.dock_area.addDock(self.settings_dock)

    def _add_plot_dock(self):
        self.plots_dock = EegPlotsDock(N_CH=GeneralSettings.N_CH)
        self.dock_area.addDock(self.plots_dock)

    def _add_saving_dock(self):
        self.saving_dock = SavingDock(external_layout=self.inner_layout)
        self.dock_area.addDock(self.saving_dock, 'top', self.plots_dock)

    def _add_banner_dock(self):
        self.banner_dock = BannerDock(external_layout=self.inner_layout)
        self.dock_area.addDock(self.banner_dock, 'top', self.plots_dock)
        self.banner_dock.hide()

    def _add_write_hardware_dock(self):
        self.write_hardware_dock = WriteHardwareDock(
            external_layout=self.inner_layout)
        self.dock_area.addDock(self.write_hardware_dock, 'top', self.plots_dock)
        self.write_hardware_dock.hide()

    def _add_pins_settings_btn(self):
        self.pins_settings_btn = RotatedButton('Pins Settings', orientation='east')
        self.layout.addWidget(self.pins_settings_btn, 0, 0)

