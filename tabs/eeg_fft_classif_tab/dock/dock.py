# -- General packages --
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
import pyqtgraph as pg
# -- My packages --
from app.colors import *
from app.activation_b import btn


class Dock:
    def __init__(self, layout):
        self.layout = layout

        plot_gr, self.plot_layout = self.create_gr()

        self.layout.addWidget(plot_gr, 0, 0)

        self.init_on_off_button()

        self.timer = QtCore.QTimer()

    def create_gr(self):
        gr = QGroupBox()
        l = QGridLayout()
        gr.setLayout(l)
        return gr, l

    def init_on_off_button(self):
        btn('Show wave signal', self.layout, (0, 0), func_conn=self.start,
            color=blue_b, toggle=True, txt_color=white)

    @pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(200)
        else:
            self.timer.stop()