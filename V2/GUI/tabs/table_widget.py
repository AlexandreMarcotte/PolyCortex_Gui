from PyQt5.QtWidgets import *
from .live_graph_tab.live_graph_tab import LiveGraphTab


class TableWidget(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_tabs()

    def add_tabs(self):
        self.addTab(LiveGraphTab(), 'Live graph')



