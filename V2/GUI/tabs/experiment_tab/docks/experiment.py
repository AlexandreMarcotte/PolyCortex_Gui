# -- General Packages --
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot

import pyqtgraph as pg
from pyqtgraph.dockarea import *

from functools import partial
from typing import Tuple


class Experiment:
    def __init__(self, timer_period=200):
        self.timer_period = timer_period

    def create_dock(self, exp_name):
        self.dock = Dock(f'{exp_name} experiment')
        self.area.addDock(self.dock, 'above', self.dock_above)

        self.layout = pg.LayoutWidget()
        self.dock.addWidget(self.layout)

        self.create_start_and_stop_b(exp_name)

    def create_plot(
                self, xs: Tuple[int, int]=(-2,7), ys: Tuple[int, int]=(-1,5),
                hide_axis=True):
        plot = pg.PlotWidget()
        plot.setXRange(*xs)
        plot.setYRange(*ys)
        if hide_axis:
            plot.hideAxis('bottom')
            plot.hideAxis('left')
        return plot

    def create_start_and_stop_b(self, exp_name):
        self.create_start_b(exp_name)
        self.create_stop_b(exp_name)

    def create_start_b(self, exp_name):
        b_start = QtGui.QPushButton(f'START {exp_name}')
        b_start.setStyleSheet("background-color: rgba(200, 200, 200, 0.5)")
        b_start.clicked.connect(partial(self.start))
        self.layout.addWidget(b_start, 0, 0)

    @pyqtSlot()
    def start(self):
        self.plot_timer.start(self.timer_period)

    def create_stop_b(self, exp_name):
        b_stop = QtGui.QPushButton(f'STOP {exp_name}')
        b_stop.setStyleSheet("background-color: rgba(200, 200, 200, 0.5)")
        b_stop.clicked.connect(partial(self.stop))
        self.layout.addWidget(b_stop, 0, 1)

    @pyqtSlot()
    def stop(self):
        self.plot_timer.stop()