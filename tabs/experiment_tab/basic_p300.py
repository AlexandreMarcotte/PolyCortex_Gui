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
from .experiment import Experiment


class BasicP300(Experiment):
    def __init__(self, area, dock_above):
        self.area = area
        self.dock_above = dock_above
        self.exp_name = 'Basic P300'

        self.plot_timer = QtCore.QTimer()

        self.create_dock()

        self.create_start_and_stop_b()

        self.plot_timer.timeout.connect(self.update_display)


    def init_dock(self):
        self.dock = Dock(self.name)
        self.area.addDock(self.dock, 'above', self.below_dock)

    def update_display(self):
        # print('hooouuuinnnn ')
        pass

