# -- My packages --
from app.colors import *
from app.activation_b import btn
from app.pyqt_frequently_used import *
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot


class Dock:
    def __init__(self, gv, layout, dock_type, dock_name):
        self.layout = layout
        self.gv = gv
        self.type = dock_type
        self.dock_name = dock_name

        self.timer = QtCore.QTimer()

    def init_on_off_button(self):
        btn(self.dock_name, self.layout, (0, 0), func_conn=self.start,
            color=blue_b, toggle=True, txt_color=white)

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
