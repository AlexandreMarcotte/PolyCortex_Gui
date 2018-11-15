# -- General packages --
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
# -- My packages --
from .groups.right_graph_layout import RightGraphLayout
from .groups.left_graph_layout import LeftGraphLayout
from .groups.file_selector import FileSelector
from tabs.static_graph_tab.updater import Updater

class StaticGraphTab:
    def __init__(self, main_window, tab_w, gv):
        self.main_window = main_window
        self.tab_w = tab_w
        self.gv = gv

        self.init_tab()

    def init_tab(self):
        self.tab_w.layout = QGridLayout(self.main_window)

        file_selector, left_panel, right_panel = self.create_grps()
        splitter = self.create_splitter(left_panel.gr, right_panel.gr)
        scroller = self.create_scroll(splitter)
        self.add_gr_to_main_widget(file_selector.gr, scroller)

        self.tab_w.setLayout(self.tab_w.layout)

        self.connect_updates(right_panel, left_panel)

    def create_grps(self):
        right_panel = RightGraphLayout(self.gv)
        left_panel = LeftGraphLayout(self.gv, right_panel)
        file_selector = FileSelector('File selector', self.main_window, self.gv,
                                     right_panel, left_panel)
        return file_selector, left_panel, right_panel

    def create_splitter(self, portion_graph_gr, full_graph_gr):
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(portion_graph_gr)
        splitter.addWidget(full_graph_gr)
        return splitter

    def create_scroll(self, splitter):
        scroller = QScrollArea()
        scroller.setWidgetResizable(True)
        scroller.setWidget(splitter)
        return scroller

    def add_gr_to_main_widget(self, file_selector_gr, scroller):
        self.tab_w.layout.addWidget(file_selector_gr)
        self.tab_w.layout.addWidget(scroller)

    def connect_updates(self, right_panel, left_panel):
        updater = Updater(self.gv)
        updater.connect_all(right_panel, left_panel, self.gv)