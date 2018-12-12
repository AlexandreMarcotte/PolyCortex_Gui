# --General Packages--
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
# --My Packages--
from tabs.eeg_fft_classif_tab.live_graph_tab import LiveGraphTab
from tabs.experiment_tab.experiment_tab import ExperimentTab
from tabs.static_graph_tab.static_graph_tab import StaticGraphTab
from tabs.mini_game_tab.mini_game_tab import MiniGameTab
# from tabs.brain_3D_tab.brain_3D_tab import Brain3DTab


class TabWidget(QWidget):
    def __init__(self, parent, gv):
        super(QWidget, self).__init__(parent)

        self.tabs_list = {LiveGraphTab(gv, parent): 'Live graph',
                          ExperimentTab(gv): 'Experiments',
                          StaticGraphTab(gv): 'Static graph',
                          MiniGameTab(): 'Mini Game'}

        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        # Add tabs
        for tab, name in self.tabs_list.items():
            self.tabs.addTab(tab, name)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
