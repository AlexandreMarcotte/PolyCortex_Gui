# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5.QtWidgets import *
from pyqtgraph.dockarea import *
# -- My packages --
from tabs.experiment_tab.emg_experiment.emg import EmgDock
from .p300 import P300Dock
from .N100 import N100Dock
from .basic_p300 import BasicP300
from .video import Video


class ExperimentTab(QWidget):
    def __init__(self, gv):
        super().__init__()
        # The second tab that was created inside the main window object
        self.gv = gv
        # Create the tab itself
        self.create_tab()
        self.create_docks()

    def create_tab(self):
        # Insert the tab layout inside the main window frame
        self.layout = QHBoxLayout(self)
        # Add docs to the tab
        self.area = DockArea()
        self.layout.addWidget(self.area)

        self.setLayout(self.layout)

    def create_docks(self):
        # EMG
        emg_dock = EmgDock(self.area, self.gv)
        # Video
        # video_dock = Video(self.area, emg_dock.emg_dock)
        # N100
        n100_dock = N100Dock(self.area, emg_dock.emg_dock)
        # P300
        p300_dock = P300Dock(self.area, emg_dock.emg_dock)
        # Basic P300
        BasicP300(self.area, emg_dock.emg_dock, self.gv)

        emg_dock.emg_dock.raiseDock()