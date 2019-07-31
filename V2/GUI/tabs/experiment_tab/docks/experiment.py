# -- General Packages --
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from functools import partial
from typing import Tuple
# -- My Packages --
from V2.utils.btn import Btn


class Experiment(Dock):
    def __init__(self, area, name='', dock_above=None, plot_timer=None,
                 timer_period=200):
        super().__init__(f'{name} experiment')
        self.area = area
        self.dock_above = dock_above
        self.timer_period = timer_period

        self._setup_dock()
        self.plot_timer = self._create_plot_timer()

    def _create_plot_timer(self):
        plot_timer = QtCore.QTimer()
        plot_timer.timeout.connect(self.update)
        return plot_timer

    def _setup_dock(self):
        if self.dock_above:
            self.area.addDock(self, 'above', self.dock_above)
        else:
            self.area.addDock(self)
        self._pg_layout = pg.LayoutWidget()
        self.addWidget(self._pg_layout)
        self._create_start_and_stop_b()
        self.plot_timer = self._init_plot_timer()

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

    def _create_start_and_stop_b(self):
        self._create_b(name='START', pos=(0, 0), conn_func=self.start)
        self._create_b(name='STOP', pos=(0, 1), conn_func=self.stop)

    def _create_b(self, name, pos, conn_func):
        b = Btn(name)
        b.clicked.connect(partial(conn_func))
        self._pg_layout.addWidget(b, *pos)

    def update(self):
        """Overload this class in the experiments classes"""

    def _init_plot_timer(self):
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
