# -- General Packages --
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

# -- My Packages --
from app.activation_b import btn
from app.pyqt_frequently_used import *


class Dock:
    def __init__(self, gv, dock_type, secondary_layout):
        self.gv = gv
        self.type = dock_type
        self.secondary_layout = secondary_layout

        self.timer = QtCore.QTimer()

    def init_choose_ch_combobox(self):
        create_param_combobox(
            self.secondary_layout, 'Channel', (0, 1),
            [str(ch+1) for ch in range(self.gv.N_CH)],
            self.print_ch, editable=False)

    def print_ch(self, ch):
        self.ch = int(ch) - 1
        print('ch: ', ch)

    def init_on_off_button(self):
        btn('Start', self.secondary_layout, (0, 0), func_conn=self.start,
            color=dark_blue_tab, toggle=True, txt_color=white, max_width=100,
            min_width=100)

    @pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(200)
        else:
            self.timer.stop()
            self.gv.freq_calculator.timer.stop()
            self.gv.freq_calculator.activated = False

        if self.type == 'fft':
            if checked:
                self.gv.freq_calculator.timer.start(100)
                self.gv.freq_calculator.activated = True
