# -- General Packages --
from PyQt5.QtWidgets import *
# -- My Packages --
from V2.GUI.tabs.static_graph_tab.view.static_graph_dock import StaticGraphDock


class ClassificationGraphDock(StaticGraphDock):
    def __init__(self, ch):
        super().__init__(ch, hide_title=False)
        self._plot, self.curve = self.init_plot(n_curves=3)
        self.region = self._init_region(self._plot)
        self._init_combobox()

    def _init_combobox(self):
        self._combobox = QComboBox()
        self._combobox.setStyleSheet(
            'QComboBox'
            # '{background-color: rgba(170, 170, 170, 200);'
            '{background-color: rgba(30, 80, 105, 120);'
            # '{background-color: rgba(20, 20, 70, 100);'
            'color:white;'
            'selection-background-color: darkblue;'
            'border: 2px solid rgba(220, 220, 220, 100);}'
            'QListView{color:red; background-color:black}')
        for val in ['1', '2', '3']:
            self._combobox.addItem(val)
        self.addWidget(self._combobox, 1, 0)

