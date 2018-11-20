# -- General Packages --
from PyQt5.QtCore import Qt, pyqtSlot
from pyqtgraph.dockarea import *
import pyqtgraph as pg
import pyqtgraph.opengl as gl              # => Try to use pyopengl directly
# from OpenGL.GL import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from functools import partial
import numpy as np
# -- My packages --
from app.colors import *


class BasicP300:
    def __init__(self, area, below_dock):
        self.name = 'Basic P300'
        self.area = area
        self.below_dock = below_dock
        self.init_dock()

    def init_dock(self):
        self.dock = Dock(self.name)
        self.area.addDock(self.dock, 'above', self.below_dock)
        Experiment(self.dock)


class Experiment:
    def __init__(self, dock):
        self.dock = dock
        self.layout = pg.LayoutWidget()
        self.dock.addWidget(self.layout)

        self.plot = self.instantiate_p300_plot()
        self.layout.addWidget(self.plot, 1, 0, 1, 2)

        self.init_timer()
        self.add_start_button()
        self.add_stop_button()

    def instantiate_p300_plot(self):
        p300_plot = pg.PlotWidget()
        p300_plot.setXRange(-2, 7)
        p300_plot.setYRange(-1, 5)
        p300_plot.hideAxis('bottom')
        p300_plot.hideAxis('left')
        return p300_plot

    def init_timer(self):
        self.timer_effect = QtCore.QTimer()
        self.timer_effect.timeout.connect(self.update_display)
        self.timer_effect.start(1000)

    def update_display(self):
        # print('hooouuuinnnn ')
        pass

    def add_start_button(self):
        b_start = QtGui.QPushButton('START P300')
        b_start.setStyleSheet("background-color: rgba(255, 255, 255, 0.5)")
        b_start.clicked.connect(partial(self.start_p300))
        self.layout.addWidget(b_start, 0, 0)

    @pyqtSlot()
    def start_p300(self):
        self.timer_effect.start(200)

    def add_stop_button(self):
        b_stop = QtGui.QPushButton('STOP P300')
        b_stop.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        b_stop.clicked.connect(partial(self.stop_p300))
        self.layout.addWidget(b_stop, 0, 1)

    @pyqtSlot()
    def stop_p300(self):
        self.timer_effect.stop()

