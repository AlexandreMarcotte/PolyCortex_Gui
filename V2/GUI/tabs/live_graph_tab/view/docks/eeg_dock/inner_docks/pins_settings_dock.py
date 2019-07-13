from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock


class PinsSettingsDock(InnerDock):
    def __init__(self, external_layout):
        super().__init__(
            name='Pin Settings', toggle_btn=True, b_checked=False,
            external_layout=external_layout, b_orientation='east',
            b_pos=(0, 0))

    def set_settings_pins_layout(self):
        pass
        # settings_pins_d = InnerDock(
        #     self.main_eeg_dock.layout, 'Pins settings', b_pos=(1, 0),
        #     toggle_button=True,
        #     size=(1, 1), b_checked=False, b_orientation='east',
        #     background_color='k')
        # self.pins_settings = []
        # for ch in range(self.main_eeg_dock.gv.N_CH):
        #     self.pins_settings.append(
        #         PinSettings(self, self.main_eeg_dock.gv,
        #                     settings_pins_d.layout, ch))
        # return settings_pins_d
#
#
