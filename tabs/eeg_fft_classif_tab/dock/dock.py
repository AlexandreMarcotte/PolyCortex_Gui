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
        self.init_plot()

        self.layout.addWidget(plot_gr, 0, 0)

        self.init_on_off_button()

        self.timer = QtCore.QTimer()

    def init_plot(self):
        plot = pg.PlotWidget(background=dark_grey)
        self.plot_layout.addWidget(plot, 1, 0)
        return plot

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
            self.timer.start(2000)
        else:
            self.timer.stop()