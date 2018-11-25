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
# Paint rectangles
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import random
# -- My packages --
from app.colors import *
from .experiment import Experiment
from app.draw_rectangle import SquareItem


class BasicP300(Experiment):
    def __init__(self, area, dock_above):
        super().__init__(timer_period=100)
        self.area = area
        self.dock_above = dock_above
        exp_name = 'Basic P300'

        self.xs = (0, 10)
        self.ys = (0, 10)

        self.plot_timer = QtCore.QTimer()
        self.create_dock(exp_name)
        # plot
        self.plot = self.create_plot(xs=self.xs, ys=self.ys)
        self.layout.addWidget(self.plot, 1, 0, 1, 2)

        self.plot_timer.timeout.connect(partial(
            self.create_rectangles_img, 10))

    def create_rectangles_img(self, n_rect):
        rand = random.randrange(30)
        if rand == 0:
            # Red
            self.clear_screen()
            p = SquareItem(
                x=np.zeros(n_rect),
                y=np.linspace(0, 15, n_rect),
                w=10 * np.ones(n_rect),
                h=0.5 * np.ones(n_rect),
                color=p300_red)
            self.refresh()
            self.plot.addItem(p)

        elif rand in (1,2,3,4,5,6):
            # Green
            self.clear_screen()
            p = SquareItem(
                x=np.linspace(0, 20, n_rect),
                y=np.zeros(n_rect),
                w=0.5 * np.ones(n_rect),
                h=10 * np.ones(n_rect),
                color=p300_green)
            self.refresh()                        # So that the graph update and the rectangle are visible
            self.plot.addItem(p)
                                            # TODO: ALEXM: Try to find a cleaner way to update the graph
        else:
            self.clear_screen()

    def clear_screen(self):
        self.plot.clear()
        self.refresh(delta_x=0.001)

    def refresh(self, delta_x=0.0):
        self.plot.setXRange(self.xs[0]+delta_x, self.xs[1])





