from tabs.live_graph_tab.dock.inner_dock import InnerDock
from ...eeg_dock.pin_settings import PinSettings


class PinsSettingDock:
    def __init__(self, main_eeg_dock):
        self.main_eeg_dock = main_eeg_dock

    def create_pins_setting_dock(self):
        settings_pins_d = self.set_settings_pins_layout()
        self.main_eeg_dock.dock_area.addDock(
                settings_pins_d.dock, 'left', self.main_eeg_dock.eeg_dock.dock)
        settings_pins_d.dock.hide()
        return settings_pins_d

    def set_settings_pins_layout(self):
        settings_pins_d = InnerDock(
                self.main_eeg_dock.layout, 'Pins settings', b_pos=(1, 0),
                toggle_button=True,
                size=(1, 1), b_checked=False, b_orientation='east',
                background_color='k')
        self.pins_settings = []
        for ch in range(self.main_eeg_dock.gv.N_CH):
            self.pins_settings.append(
                PinSettings(self, self.main_eeg_dock.gv,
                            settings_pins_d.layout, ch))
        return settings_pins_d


