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
        self.exp_name = 'Basic P300'

        self.plot_timer = QtCore.QTimer()
        self.create_dock()
        self.create_start_and_stop_b()

        self.plot_timer.timeout.connect(self.update_display)

    def update_display(self):
        rand = random.randrange(30)
        if rand == 0:
            self.clear_screen()
            p = SquareItem(
                x=np.zeros(10),
                y=np.linspace(0, 5, 10),
                w=4 * np.ones(10),
                h=0.1 * np.ones(10),
                color=p300_red)
            self.plot.addItem(p)
            self.plot.setXRange(-2, 7)

        elif rand in (1,2,3,4,5,6):
            self.clear_screen()
            p = SquareItem(
                x=np.linspace(0, 5, 10),
                y=np.zeros(10),
                w=0.1 * np.ones(10),
                h=4 * np.ones(10),
                color=p300_green)
            self.plot.addItem(p)
            self.plot.setXRange(-2, 7)      # So that the graph update and the rectangle are visible
                                            # TODO: ALEXM: Try to find a cleaner way to update the graph
        else:
            self.clear_screen()

    def clear_screen(self):
        self.plot.clear()
        self.plot.setXRange(-2, 7.1)





