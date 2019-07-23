from PyQt5.QtWidgets import *
from V2.GUI.tabs.live_graph_tab.controller.live_graph_tab import LiveGraphTab


class TableWidget(QTabWidget):
    """ Control the creation of the tabs"""
    def __init__(self, main_window):
        super().__init__(main_window)

        self.add_tabs()

    def add_tabs(self):
        self.live_graph_tab = LiveGraphTab()._view
        self.addTab(self.live_graph_tab, 'Live graph')
        # self.addTab(LiveGraphTabController()._view, 'Experiment')
