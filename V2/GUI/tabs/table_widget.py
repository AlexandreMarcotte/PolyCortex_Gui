from PyQt5.QtWidgets import *
from V2.GUI.tabs.experiment_tab.experiment_tab import ExperimentTabView
from V2.GUI.tabs.model.model import Model
from V2.GUI.tabs.live_graph_tab.view.live_graph_tab_view import LiveGraphTabView
from V2.GUI.tabs.controller.controller import Controller


class TableWidget(QTabWidget):
    """ Control the creation of the tabs"""
    def __init__(self, main_window):
        super().__init__(main_window)

        self._model = Model()
        self.controller = Controller(self._model)
        # View
        self.live_graph_tab = LiveGraphTabView(self._model, self.controller)
        self.experiment_tab = ExperimentTabView(self._model, self.controller)

        self.add_tabs()

    def add_tabs(self):
        self.addTab(self.live_graph_tab, 'Live graph')
        self.addTab(self.experiment_tab, 'Experiment')

