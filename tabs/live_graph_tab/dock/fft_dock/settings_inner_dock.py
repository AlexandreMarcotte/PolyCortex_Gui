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
    def __init__(self, gv, parent):
        super().__init__(
                parent.layout, 'Settings', toggle_button=True, size=(1, 1))
        self.gv = gv
        self.parent = parent

        self.ch_to_show = list(range(self.gv.N_CH))

        self.add_combobox_to_inner_dock()

    def add_combobox_to_inner_dock(self):
        self.add_on_off_button()
        self.add_max_freq_combobox()
        self.add_max_microV_combobox()
        self.add_log_combobox()
        self.add_filter_combobox()
        self.add_ch_on_combobox()
        self.add_log_combobox()

    def add_on_off_button(self):
        self.timer = self.init_timer()
        btn('Start', self.layout, (0, 0), func_conn=self.start,
            color=dark_blue_tab, toggle=True, txt_color=white, min_width=100)

    def init_timer(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update_plotting)
        return timer

    def update_plotting(self):
        self.all_frequency()

    def all_frequency(self):
        for ch in self.ch_to_show:
            f_range, fft = self.gv.freq_calculator.get_fft_to_plot(
                np.array(self.gv.data_queue[ch])[
                self.gv.filter_min_bound: self.gv.filter_max_bound])
            self.parent.freq_curves[ch].setData(f_range, fft)

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        if checked:
            if not self.gv.freq_calculator.activated:
                self.gv.freq_calculator.timer.start(100)
                self.gv.freq_calculator.activated = True
            self.timer.start(100)
        else:
            self.timer.stop()
            self.gv.freq_calculator.timer.stop()
            self.gv.freq_calculator.activated = False

    def add_max_freq_combobox(self):
        create_param_combobox(
                self.layout, 'Max Freq', (0, 1),
                ['Auto', '60 Hz', '80 Hz', '100 Hz', '120 Hz'],
                partial(self.scale_axis, axis_name='x'))

    def add_max_microV_combobox(self):
        create_param_combobox(
                self.layout, 'Max Uv', (0, 2),
                ['Auto','1000 uv', '10000 uv', '100000 uv', '1000000 uv',
                 '10000000 uv'], partial(self.scale_axis, axis_name='y'))

    def scale_axis(self, txt, axis_name):
        try:
            if txt == 'Auto':
                self.parent.plot.enableAutoRange()
            else:
                r = int(re.search(r'\d+', txt).group())
                if axis_name == 'x':
                    self.parent.plot.setXRange(0, r)
                elif axis_name == 'y':
                    self.parent.plot.setYRange(0, r)
        except AttributeError:
            print("Come on bro, this  value doesn't make sens")

    def add_log_combobox(self):
        create_param_combobox(
                self.layout, 'Log', (0, 3), ['False', 'True'],
                self.log_axis)

    def log_axis(self, txt):
        self.parent.plot.setLogMode(y=eval(txt))

    def add_filter_combobox(self):
        create_param_combobox(
                self.layout, 'Filter', (0, 4), ['No filter',
                'Bandpass', 'Bandstop', 'Both'], self.show_filter)

        self.combo_to_filter = {
                'No filter': [], 'Bandpass': ['bandpass'],
                'Bandstop': ['bandstop'], 'Both': ['bandpass', 'bandstop']}

    def show_filter(self, txt):
        self.gv.filter_to_use = self.combo_to_filter[txt]

    def add_ch_on_combobox(self):
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
        for c in self.parent.freq_curves:
            c.clear()

