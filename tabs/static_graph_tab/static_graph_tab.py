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
        full_graph = FullGraph(1)
        portion_graph = PortionGraph()
        file_selection = FileSelection(self.main_window, self.gv)
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


class Group:
    def __init__(self):
        self.name = 'Group'

    def create_grp(self):
        layout = QGridLayout()
        grp = QGroupBox(self.name)
        grp.setLayout(layout)
        return grp, layout


# -- General packages--
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from functools import partial
# -- My packages --
from app.colors import *
from generate_signal.from_file import read_data_from_file

class FileSelection(Group):
    def __init__(self, win, gv):
        super().__init__()
        self.win = win
        self.gv = gv

        self.file_name = './experiment_csv/2exp_pinch_close_2018-08-29 19:44:54.567417.csv'
        self.name = 'Open file'

        self.grp, self.layout = self.create_grp()
        self.path_line_edit = self.init_layout()

    def init_layout(self):
        self.add_choose_file_b()
        self.add_open_file_b()
        path_line_edit = self.add_data_path_line_edit()
        return path_line_edit

    def add_choose_file_b(self):
        b = QtGui.QPushButton('Choose file containing data')
        b.setStyleSheet(f'background-color: {blue_b}')
        b.clicked.connect(partial(self.open_static_data_file))
        self.layout.addWidget(b, 0, 0)

    def add_open_file_b(self):
        open_file_b = QtGui.QPushButton('Open File')
        open_file_b.clicked.connect(partial(self.create_stationnary_plot))
        self.layout.addWidget(open_file_b, 0, 2)

    def add_data_path_line_edit(self):
        """Create text box to show or enter path to data file"""
        path_line_edit = QtGui.QLineEdit(self.file_name)
        self.layout.addWidget(path_line_edit, 0, 1)
        return path_line_edit

    @pyqtSlot()
    def open_static_data_file(self):
        # From: https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self.win, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            self.path_line_edit.setText(file_name)
            self.file_name = file_name

    @pyqtSlot()
    def create_stationnary_plot(self):
        # Read data from file
        data, t, exp = read_data_from_file(self.path_line_edit.text(),
                                           n_ch=self.gv.N_CH)


class PortionGraph(Group):
    def __init__(self):
        super().__init__()
        self.name = 'Portion graph'

        self.grp, self.layout = self.create_grp()


import pyqtgraph as pg

class AllFullGraph:
    def __init__(self):
        pass

class FullGraph(Group):
    def __init__(self, ch):
        super().__init__()
        self.ch = ch

        self.name = 'Full graph'
        self.x_range = 8000

        self.grp, self.layout = self.create_grp()
        self.add_graph()

    def add_graph(self):
        layout = QGridLayout()
        box = QGroupBox(f'{self.ch}')
        box.setLayout(layout)
        region = pg.LinearRegionItem()
        plot = pg.PlotWidget()
        plot.setXRange(0, self.x_range)
        self.layout.addWidget(plot, self.ch, 0)


