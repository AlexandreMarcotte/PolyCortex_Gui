# -- General Packages --
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from functools import partial
from typing import Tuple


class Experiment:
    def __init__(self, area, name='', dock_above=None, plot_timer=None,
                 timer_period=200):
        self.area = area
        self.dock_above = dock_above
        self.timer_period = timer_period

        self.create_dock(name)
        self.plot_timer = self._create_plot_timer()

    def _create_plot_timer(self):
        plot_timer = QtCore.QTimer()
        plot_timer.timeout.connect(self.update)
        return plot_timer

    def create_dock(self, exp_name):
        self.dock = Dock(f'{exp_name} experiment')
        if self.dock_above:
            self.area.addDock(self.dock, 'above', self.dock_above)
        else:
            self.area.addDock(self.dock)

        self.layout = pg.LayoutWidget()
        self.dock.addWidget(self.layout)

        self.create_start_and_stop_b()
        self.init_plot_timer()

    def create_plot(
                self, xs: Tuple[int, int]=None, ys: Tuple[int, int]=None,
                hide_axis=True):
        plot = pg.PlotWidget()
        if xs:
            plot.setXRange(*xs)
        if ys:
            plot.setYRange(*ys)
        if hide_axis:
            plot.hideAxis('bottom')
            plot.hideAxis('left')
        return plot

    def create_start_and_stop_b(self):
        self.create_b(name='START', pos=(0, 0), conn_func=self.start)
        self.create_b(name='STOP', pos=(0, 1), conn_func=self.stop)

    def create_b(self, name, pos, conn_func):
        b = QtGui.QPushButton(name)
        b.setStyleSheet("background-color: rgba(200, 200, 200, 0.5)")
        b.clicked.connect(partial(conn_func))
        self.layout.addWidget(b, *pos)

    def update(self):
        """Overload this class in the experiments classes"""

    def init_plot_timer(self):
        plot_timer = QtCore.QTimer()
        plot_timer.timeout.connect(self.update)
        return plot_timer

    @pyqtSlot()
    def start(self):
        self.plot_timer.start(self.timer_period)

    @pyqtSlot()
    def stop(self):
        self.plot_timer.stop()

    def connect_signal_collector(self, signal_collector):
        self.signal_collector = signal_collector
