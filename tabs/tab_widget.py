# --General Packages--
from PyQt5.QtWidgets import QTabWidget
# --My Packages--
from tabs.live_graph_tab.live_graph_tab import LiveGraphTab
from tabs.experiment_tab.experiment_tab import ExperimentTab
from tabs.static_graph_tab.static_graph_tab import StaticGraphTab
from tabs.game_3D_tab.game_3D_tab import Game3DTab
from tabs.machine_learning_tab.machine_learning_tab import MachineLearningTab


class TabWidget(QTabWidget):
    def __init__(self, parent, gv):
        super().__init__(parent)

        self.tabs_list = {
                LiveGraphTab(gv, parent): 'Live graph',
                ExperimentTab(gv): 'Experiments',
                StaticGraphTab(gv): 'Static graph',
                MachineLearningTab(gv): 'Machine learning',
                Game3DTab(): '3D Game'}

        for tab, name in self.tabs_list.items():
            self.addTab(tab, name)