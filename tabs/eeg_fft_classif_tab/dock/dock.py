from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
import pyqtgraph as pg
from app.colors import *


class Dock:
    def __init__(self):
        self.timer = QtCore.QTimer()
        self.init_plot()

    def init_plot(self):
        self.plot = pg.PlotWidget(background=dark_grey)

    def create_gr(self):
        gr = QGroupBox()
        l = QGridLayout()
        gr.setLayout(l)
        return gr, l

    @pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(100)
        else:
            self.timer.stop()