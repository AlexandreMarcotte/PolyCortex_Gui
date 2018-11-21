# -- General Packages --
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import *

import pyqtgraph as pg
from pyqtgraph.dockarea import *

from functools import partial
from random import randint


class Experiment:

    def create_dock(self):
        self.dock = Dock(f'{self.exp_name}')
        self.area.addDock(self.dock, 'above', self.dock_above)

        self.plot = self.create_plot()
        self.dock.addWidget(self.plot, 1, 0, 1, 2)

        self.create_start_and_stop_b()

    def create_plot(self):
        plot = pg.PlotWidget()
        plot.setXRange(-2, 7)
        plot.setYRange(-1, 5)
        plot.hideAxis('bottom')
        plot.hideAxis('left')
        return plot

    def create_start_and_stop_b(self):
        self.create_start_b()
        self.create_stop_b()

    def create_start_b(self):
        b_start = QtGui.QPushButton('START P300')
        b_start.setStyleSheet("background-color: rgba(200, 200, 200, 0.5)")
        b_start.clicked.connect(partial(self.start))
        self.dock.addWidget(b_start, 0, 0)

    @pyqtSlot()
    def start(self):
        self.timer.start(200)

    def create_stop_b(self):
        b_stop = QtGui.QPushButton('STOP P300')
        b_stop.setStyleSheet("background-color: rgba(200, 200, 200, 0.5)")
        b_stop.clicked.connect(partial(self.stop))
        self.dock.addWidget(b_stop, 0, 1)

    @pyqtSlot()
    def stop(self):
        self.timer.stop()