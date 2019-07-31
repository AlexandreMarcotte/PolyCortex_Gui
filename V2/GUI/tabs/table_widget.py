# -- General Packages --
from PyQt5.QtWidgets import *
# -- My Packages --
from .experiment_tab.experiment_tab_view import ExperimentTabView
from .live_graph_tab.view.live_graph_tab_view import LiveGraphTabView
from V2.GUI.tabs.static_graph_tab.view.static_graph_tab_view import StaticGraphTabView
from .model.model import Model
from .controller.controller import Controller



class TableWidget(QTabWidget):
    """ Control the creation of the tabs"""
    def __init__(self, main_window):
        super().__init__(main_window)

        self._model = Model()
        self.controller = Controller(self._model)

        self._create_tabs()
        self._add_tabs()

    def _create_tabs(self):
        self.live_graph_tab = LiveGraphTabView(self._model, self.controller)
        self.experiment_tab = ExperimentTabView(self._model, self.controller)
        self.static_graph_tab = StaticGraphTabView(self._model, self.controller)

    def _add_tabs(self):
        self.addTab(self.live_graph_tab, 'Live Graph')
        self.addTab(self.experiment_tab, 'Experiment')
        self.addTab(self.static_graph_tab, 'Static Graph')

