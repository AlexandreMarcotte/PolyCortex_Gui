# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import *

from pyqtgraph.dockarea import *

import pyqtgraph as pg
from functools import partial

from random import randint

# -- My packages --
from .action import Action
from .p300 import P300Dock
from .emg import EmgDock
from .N100 import N100Dock
from .basic_p300 import BasicP300
from app.colors import *


class ExperimentTab(QWidget):
    def __init__(self, gv):
        super().__init__()
        # The second tab that was created inside the main window object
        self.gv = gv
        # Create the tab itself
        self.create_tab()

    def create_tab(self):
        # Insert the tab layout inside the main window frame
        self.layout = QHBoxLayout(self)
        # Add docs to the tab
        self.area = DockArea()
        self.layout.addWidget(self.area)

        self.create_docks()

        self.setLayout(self.layout)

    def create_docks(self):
        # EMG
        emg_dock = EmgDock(self.area, self.gv)
        # N100
        n100_dock = N100Dock(self.area, emg_dock.emg_dock)
        # P300
        p300_dock = P300Dock(self.area, emg_dock.emg_dock)
        # Basic P300
        BasicP300(self.area, emg_dock.emg_dock)