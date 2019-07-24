from PyQt5.QtWidgets import *
from .live_graph_tab.controller.live_graph_tab import LiveGraphTab
from .experiment_tab.experiment_tab import ExperimentTab


class TableWidget(QTabWidget):
    """ Control the creation of the tabs"""
    def __init__(self, main_window):
        super().__init__(main_window)

        self.add_tabs()

    def add_tabs(self):
        self.live_graph_tab = LiveGraphTab()._view
        self.addTab(self.live_graph_tab, 'Live graph')
        # self.addTab(LiveGraphTabController()._view, 'Experiment')
        self.experiment_tab = ExperimentTab()
        self.addTab(self.experiment_tab, 'Experiment')

