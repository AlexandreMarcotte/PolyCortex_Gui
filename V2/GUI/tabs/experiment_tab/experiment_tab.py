# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5.QtWidgets import *
from pyqtgraph.dockarea import *
# -- My packages --
from tabs.experiment_tab.emg_experiment.emg import EmgDock
from V2.GUI.tabs.experiment_tab.docks.p300 import P300Dock
from V2.GUI.tabs.experiment_tab.docks.basic_p300 import BasicP300
from .connectors.experiment_connector import ExperimentConnector


class ExperimentTabView(QWidget):
    def __init__(self, model, controller):
        super().__init__()

        self.model = model
        self.controller = controller

        self._init_ui()
        self._connect()

    def _connect(self):
        self.experiment_connector = ExperimentConnector(
            view=self, model=self.model)

    def _init_ui(self):
        # The second tab that was created inside the main window object
        # Create the tab itself
        self._init_tab()
        self._init_docks()

    def _init_tab(self):
        # Insert the tab layout inside the main window frame
        self.layout = QHBoxLayout(self)
        # Add docs to the tab
        self.area = DockArea()
        self.layout.addWidget(self.area)

        self.setLayout(self.layout)

    def _init_docks(self):
        # EMG
        emg_dock = EmgDock(self.area)
        # Video
        # video_dock = Video(self.area, emg_dock.emg_dock)
        # N100
        # n100_dock = N100Dock(self.area, emg_dock.emg_dock)
        # P300
        p300_dock = P300Dock(self.area, emg_dock.emg_dock)
        # Basic P300
        BasicP300(self.area, emg_dock.emg_dock)

        # emg_dock.emg_dock.raiseDock()
