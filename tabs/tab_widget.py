from PyQt5.QtWidgets import *
# -- Tabs --
from tabs.eeg_fft_classif_tab.eeg_fft_classif_tab import EegFftClassifTab
from tabs.experiment_tab.experiment_tab import ExperimentTab
from tabs.static_graph_tab.static_graph_tab import StaticGraphTab
from tabs.mini_game_tab.mini_game_tab import MiniGameTab
from tabs.brain_3D_tab.brain_3D_tab import Brain3DTab


class TabWidget(QWidget):                                                     # TODO: ALEXM, Change the name of this class so that it fit the model of all the class that are include inside each other in the pyqt framework
    def __init__(self, gv):
        """
        """
        super().__init__()
        self.gv = gv
        self.init_win()

    def init_win(self):
        """Create the layout ant add all the required tabs to it"""
        layout = QVBoxLayout(self)

        tabs_w_list = QTabWidget()
        tabs_w = []

        tabs_name = ['EEG & FFT live graph', 'Experiments', 'EEG static graph',
                     'Mini Game', '3D brain']
        tabs_class = [EegFftClassifTab, ExperimentTab, StaticGraphTab,
                      MiniGameTab, Brain3DTab]

        for i, tab_name in enumerate(tabs_name):
            tabs_w.append(QWidget())
            tabs_w_list.addTab(tabs_w[i], tab_name)
            if i <= 2:
                tabs_class[i](self, tabs_w[i], self.gv)
            else:
                tabs_class[i](self, tabs_w[i])

        # Add tabs to widget
        layout.addWidget(tabs_w_list)
        self.setLayout(layout)