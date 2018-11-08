# -- General packages --
# Graph
from PyQt5.QtWidgets import *


class StaticGraphTab:
    def __init__(self, main_window, tab_w, gv):
        self.main_window = main_window
        self.tab_w = tab_w
        self.gv = gv

    def create_tab(self):
        self.tab_w.layout = QGridLayout(self.main_window)