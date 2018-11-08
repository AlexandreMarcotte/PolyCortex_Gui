# -- General packages --
# Graph
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class StaticGraphTab:
    def __init__(self, main_window, tab_w, gv):
        self.main_window = main_window
        self.tab_w = tab_w
        self.gv = gv

        self.init_tab()

    def init_tab(self):
        self.tab_w.layout = QGridLayout(self.main_window)

        file_selection, portion_graph, full_graph = self.create_grps()
        splitter = self.create_splitter(portion_graph, full_graph)
        scroller = self.create_scroll(splitter)
        self.add_grp_to_main_widget(file_selection, scroller)

        self.tab_w.setLayout(self.tab_w.layout)

    def create_grps(self):
        full_graph = FullGraph()
        portion_graph = PortionGraph()
        file_selection = FileSelection()
        return file_selection, portion_graph, full_graph

    def create_splitter(self, portion_graph, full_graph):
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(portion_graph.grp)
        splitter.addWidget(full_graph.grp)
        return splitter

    def create_scroll(self, splitter):
        scroller = QScrollArea()
        scroller.setWidgetResizable(True)
        scroller.setWidget(splitter)
        return scroller

    def add_grp_to_main_widget(self, file_selection, scroller):
        self.tab_w.layout.addWidget(file_selection.grp)
        self.tab_w.layout.addWidget(scroller)


class PortionGraph:
    def __init__(self):
        self.name = 'Portion graph'
        self.grp = self.create_grp()

    def create_grp(self):
        layout = QGridLayout()
        grp = QGroupBox(self.name)
        grp.setLayout(layout)
        return grp


class FileSelection:
    def __init__(self):
        self.name = 'Open file'
        self.grp = self.create_grp()

    def create_grp(self):
        layout = QGridLayout()
        grp = QGroupBox(self.name)
        grp.setLayout(layout)
        return grp
    

class FullGraph: 
    def __init__(self):
        self.name = 'Full graph'
        self.grp = self.create_grp()
    
    def create_grp(self):
        layout = QGridLayout()
        grp = QGroupBox(self.name)
        grp.setLayout(layout)
        return grp