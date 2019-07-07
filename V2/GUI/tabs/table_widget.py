from PyQt5.QtWidgets import *
from V2.GUI.tabs.live_graph_tab.controller.live_graph_tab_controller import LiveGraphTabController


class TableWidget(QTabWidget):
    """ Control the creation of the tabs"""
    def __init__(self, parent):
        super().__init__(parent)

        self.add_tabs()

    def add_tabs(self):
        self.addTab(LiveGraphTabController()._view, 'Live graph')
