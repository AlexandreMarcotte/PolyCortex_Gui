#--General Packages--
from PyQt5 import QtCore
#--My Packages--
from app.activation_b import btn
from app.colors import *


class StartButton:
    def __init__(self, gv, plot_inner_dock, layout):
        self.gv = gv

        self.timer = plot_inner_dock.init_timer()
        btn('Start', layout, (0, 0), func_conn=self._start,
            color=dark_blue_tab, toggle=True, txt_color=white, min_width=100)

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

