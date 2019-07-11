# -- My Packages --
from V2.utils.parameter_combobox import ParameterCombobox
from V2.GUI.tabs.live_graph_tab.view.docks.inner_docks.settings_dock import SettingsDock


class FftSettingsDock(SettingsDock):
    def __init__(self, main_layout):
        super().__init__(main_layout)

        self.main_layout = main_layout

        self._create_settings_dock()

    def _create_settings_dock(self):
        super()._create_settings_dock()
        # Plot parameter
        self._create_all_combobox()

    def _create_all_combobox(self):
        self.scale_axis_cb = ParameterCombobox(
            self.inner_layout, 'Max Freq', (0, 1),
            ['Auto', '60 Hz', '80 Hz', '100 Hz', '120 Hz'])
        self.max_microV_cb = ParameterCombobox(
            self.inner_layout, 'Max Uv', (0, 2), ['Auto', '1000 uv', '10000 uv',
            '100000 uv', '1000000 uv', '10000000 uv'], editable=False)
        self.log_cb = ParameterCombobox(
            self.inner_layout, 'Log', (0, 3), ['False', 'True'], editable=False)
        self.filter_cb = ParameterCombobox(
            self.inner_layout, 'Filter', (0, 4), ['No filter', 'Bandpass',
            'Bandstop', 'Both'], editable=False)
        self.ch_on_cb = ParameterCombobox(
            self.inner_layout, 'Ch On/Off', (0, 5), ['ch 1', 'ch 2', 'ch 3', 'ch 4',
            'ch 5', 'ch 6', 'ch 7', 'ch 8', 'all'], editable=False)





