# --General Packages--
from functools import partial
import re
from PyQt5 import QtCore
import numpy as np
# --My Packages--
from app.pyqt_frequently_used import create_param_combobox
from tabs.live_graph_tab.dock.inner_dock import InnerDock
from app.activation_b import btn
from app.colors import *


class SettingsInnerDock(InnerDock):
    def __init__(self, gv, parent, plot_inner_dock):
        super().__init__(
                parent.layout, 'Settings', toggle_button=True, size=(1, 1))
        self.gv = gv
        self.plot_inner_dock = plot_inner_dock

        self.ch_to_show = list(range(self.gv.N_CH))

        self._add_combobox_to_inner_dock()

    def _add_combobox_to_inner_dock(self):
        self._add_on_off_button()
        self._add_max_freq_combobox()
        self._add_max_microV_combobox()
        self._add_log_combobox()
        self._add_filter_combobox()
        self._add_ch_on_combobox()
        self._add_log_combobox()

    def _add_on_off_button(self):
        self.timer = self._init_timer()
        btn('Start', self.layout, (0, 0), func_conn=self._start,
            color=dark_blue_tab, toggle=True, txt_color=white, min_width=100)

    def _init_timer(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self._update_plotting)
        return timer

    def _update_plotting(self):
        self._all_frequency()

    def _all_frequency(self):
        for ch in self.ch_to_show:
            f_range, fft = self.gv.freq_calculator.get_fft_to_plot(
                np.array(self.gv.data_queue[ch])[
                self.gv.filter_min_bound: self.gv.filter_max_bound])
            self.plot_inner_dock.freq_curves[ch].setData(f_range, fft)

    @QtCore.pyqtSlot(bool)
    def _start(self, checked):
        if checked:
            if not self.gv.freq_calculator.activated:
                self.gv.freq_calculator.timer.start(100)
                self.gv.freq_calculator.activated = True
            self.timer.start(100)
        else:
            self.timer.stop()
            self.gv.freq_calculator.timer.stop()
            self.gv.freq_calculator.activated = False

    def _add_max_freq_combobox(self):
        create_param_combobox(
                self.layout, 'Max Freq', (0, 1),
                ['Auto', '60 Hz', '80 Hz', '100 Hz', '120 Hz'],
                partial(self.scale_axis, axis_name='x'))

    def _add_max_microV_combobox(self):
        create_param_combobox(
                self.layout, 'Max Uv', (0, 2),
                ['Auto','1000 uv', '10000 uv', '100000 uv', '1000000 uv',
                 '10000000 uv'], partial(self.scale_axis, axis_name='y'))

    def scale_axis(self, txt, axis_name):
        try:
            if txt == 'Auto':
                self.plot_inner_dock.plot.enableAutoRange()
            else:
                r = int(re.search(r'\d+', txt).group())
                if axis_name == 'x':
                    self.plot_inner_dock.plot.setXRange(0, r)
                elif axis_name == 'y':
                    self.plot_inner_dock.plot.setYRange(0, r)
        except AttributeError:
            print("Come on bro, this  value doesn't make sens")

    def _add_log_combobox(self):
        create_param_combobox(
                self.layout, 'Log', (0, 3), ['False', 'True'],
                self.log_axis)

    def log_axis(self, txt):
        self.plot_inner_dock.plot.setLogMode(y=eval(txt))

    def _add_filter_combobox(self):
        create_param_combobox(
                self.layout, 'Filter', (0, 4), ['No filter',
                'Bandpass', 'Bandstop', 'Both'], self.show_filter)

        self.combo_to_filter = {
                'No filter': [], 'Bandpass': ['bandpass'],
                'Bandstop': ['bandstop'], 'Both': ['bandpass', 'bandstop']}

    def show_filter(self, txt):
        self.gv.filter_to_use = self.combo_to_filter[txt]

    def _add_ch_on_combobox(self):
        create_param_combobox(
                self.layout, 'Ch On', (0, 5),
                ['ch 1', 'ch 2', 'ch 3', 'ch 4',
                 'ch 5', 'ch 6', 'ch 7', 'ch 8', 'all'],
                self.ch_on_off, editable=False)

    def ch_on_off(self, ch):
        if ch == 'all':
            self.ch_to_show = list(range(self.gv.N_CH))
        else:
            self.ch_to_show = [int(ch[3:]) - 1]
        self.clear_curves()

    def clear_curves(self):
        for c in self.plot_inner_dock.freq_curves:
            c.clear()

