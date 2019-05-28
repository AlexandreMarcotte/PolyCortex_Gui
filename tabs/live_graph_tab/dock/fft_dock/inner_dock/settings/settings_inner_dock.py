# --My Packages--
from tabs.live_graph_tab.dock.inner_dock import InnerDock
from .combobox.scale_axis_combobox import ScaleAxisCombobox
from .combobox.log_combobox import LogCombobox
from .combobox.filter_combobox import FilterCombobox
from .combobox.ch_on_combobox import ChOnCombobox
from .start_button import StartButton




class SettingsInnerDock(InnerDock):
    def __init__(self, gv, parent, plot_inner_dock):
        super().__init__(
                parent.layout, 'Settings', toggle_button=True, size=(1, 1))
        self.gv = gv
        self.plot_inner_dock = plot_inner_dock

        self._add_combobox_to_inner_dock()

    def _add_combobox_to_inner_dock(self):
        self._add_start_button()
        self._add_max_freq_combobox()
        self._add_max_microV_combobox()
        self._add_log_combobox()
        self._add_filter_combobox()
        self._add_ch_on_combobox()

    def _add_start_button(self):
        StartButton(self.gv, self.plot_inner_dock, self.layout)

    def _add_max_freq_combobox(self):
        ScaleAxisCombobox(
                self.plot_inner_dock, self.layout, 'Max Freq', (0, 1),
                ['Auto', '60 Hz', '80 Hz', '100 Hz', '120 Hz'], axis_name='x')

    def _add_max_microV_combobox(self):
       ScaleAxisCombobox(
                self.plot_inner_dock, self.layout, 'Max Uv', (0, 2),
                ['Auto','1000 uv', '10000 uv', '100000 uv', '1000000 uv',
                 '10000000 uv'], axis_name='y')

    def _add_log_combobox(self):
        LogCombobox(
                plot_inner_dock=self.plot_inner_dock, layout=self.layout,
                name='Log', pos=(0, 3), param=['False', 'True'])

    def _add_filter_combobox(self):
        FilterCombobox(
                gv=self.gv, plot_inner_dock=self.plot_inner_dock,
                layout=self.layout, name='Filter', pos=(0, 4),
                param=['No filter', 'Bandpass', 'Bandstop', 'Both'])

    def _add_ch_on_combobox(self):
        ChOnCombobox(
                gv=self.gv, plot_inner_dock=self.plot_inner_dock,
                layout=self.layout, name='Ch On/Off', pos=(0, 6),
                param=['ch 1', 'ch 2', 'ch 3', 'ch 4',
                       'ch 5', 'ch 6', 'ch 7', 'ch 8', 'all'])


