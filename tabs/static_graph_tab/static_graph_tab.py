# -- General packages --
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
# -- My packages --
from .groups.right_graph_layout import RightGraphLayout
from .groups.left_graph_layout import LeftGraphLayout
from .groups.file_selector import FileSelector
from tabs.static_graph_tab.updater import Updater


class StaticGraphTab(QWidget):
    def __init__(self, gv):
        super().__init__()
        self.gv = gv

        self.init_tab()

    def init_tab(self):
        self.layout = QGridLayout(self)

        file_selector, left_panel, right_panel = self.create_grps()
        splitter = self.create_splitter(left_panel.gr, right_panel.gr)
        scroller = self.create_scroll(splitter)
        self.add_gr_to_main_widget(file_selector.gr, scroller)

        self.setLayout(self.layout)

        self.connect_updates(right_panel, left_panel)

    def create_grps(self):
        right_panel = RightGraphLayout(self.gv)
        left_panel = LeftGraphLayout(self.gv, right_panel)
        file_selector = FileSelector('File selector', self, self.gv,
                                     right_panel, left_panel)
        return file_selector, left_panel, right_panel

    def create_splitter(self, portion_graph_gr, full_graph_gr):
        sp = QSplitter(Qt.Horizontal)
        sp.addWidget(portion_graph_gr)
        sp.addWidget(full_graph_gr)
        return sp

    def create_scroll(self, splitter):
        sc = QScrollArea()
        sc.setWidgetResizable(True)
        sc.setWidget(splitter)
        return sc

    def add_gr_to_main_widget(self, file_selector_gr, scroller):
        self.layout.addWidget(file_selector_gr)
        self.layout.addWidget(scroller)

    def connect_updates(self, right_panel, left_panel):
        updater = Updater(self.gv)
        updater.connect_all(right_panel, left_panel, self.gv)