# --My packages--
from V2.utils.my_dock import MyDock
from ..eeg_dock.inner_docks.settings_dock import SettingsDock
from ..eeg_dock.inner_docks.eeg_plots_dock import EegPlotsDock


class EegDock(MyDock):
    def __init__(self, upper):
        super().__init__('EEG_dock')
        self.upper = upper
        self.init_settings_inner_dock()
        self.init_eeg_plots_dock()

    def init_settings_inner_dock(self):
        settings_dock = SettingsDock(self.layout)
        self.dock_area.addDock(settings_dock.dock)

    def init_eeg_plots_dock(self):
        eeg_plots_dock = EegPlotsDock()
        self.dock_area.addDock(eeg_plots_dock)


