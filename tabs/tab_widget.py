from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from tabs.eeg_fft_classif_tab.eeg_fft_classif_tab import EegFftClassifTab
from tabs.experiment_tab.experiment_tab import ExperimentTab
from tabs.static_graph_tab.static_graph_tab import StaticGraphTab
from tabs.mini_game_tab.mini_game_tab import MiniGameTab
from tabs.brain_3D_tab.brain_3D_tab import Brain3DTab


class TabWidget(QWidget):
    def __init__(self, parent, gv):
        super(QWidget, self).__init__(parent)

        self.tabs_list = {EegFftClassifTab(gv): 'EEG & FFT live graph',
                          ExperimentTab(gv): 'Experiments',
                          StaticGraphTab(gv): 'EEG static graph',
                          MiniGameTab(): 'Mini Game',
                          Brain3DTab(): '3D brain'}

        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()

        # Add tabs
        for tab, name in self.tabs_list.items():
            self.tabs.addTab(tab, name)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
