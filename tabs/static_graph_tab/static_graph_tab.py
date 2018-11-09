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

        file_selection_gr, portion_graph_gr, full_graph_gr = self.create_grps()
        splitter = self.create_splitter(portion_graph_gr, full_graph_gr)
        scroller = self.create_scroll(splitter)
        self.add_gr_to_main_widget(file_selection_gr, scroller)

        self.tab_w.setLayout(self.tab_w.layout)

    def create_grps(self):
        file_selection_gr = self.create_file_selection_gr()
        portion_graph_gr = self.create_portion_graph_gr()
        full_graph_gr = self.create_full_graph_gr()
        return file_selection_gr, portion_graph_gr, full_graph_gr

    def create_file_selection_gr(self):
        file_selection_gr = Group('File selection')
        FileSelection(self.main_window, self.gv, file_selection_gr.layout)
        return file_selection_gr.gr

    def create_portion_graph_gr(self):
        portion_graph_gr = Group('Portion graph')
        PortionGraph(portion_graph_gr.layout)
        return portion_graph_gr.gr

    def create_full_graph_gr(self):
        full_graph_gr = Group('Full graph')
        for i in range(self.gv.N_CH):
            FullGraph(self.gv, i, full_graph_gr.layout)
        return full_graph_gr.gr

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

    def add_gr_to_main_widget(self, file_selection_gr, scroller):
        self.tab_w.layout.addWidget(file_selection_gr)
        self.tab_w.layout.addWidget(scroller)




class Group:
    def __init__(self, name):
        self.name = name
        self.layout, self.gr = self.create_gr()

    def create_gr(self):
        layout = QGridLayout()
        gr = QGroupBox(self.name)
        gr.setLayout(layout)
        return layout, gr


# -- General packages--
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from functools import partial
# -- My packages --
from app.colors import *
from generate_signal.from_file import read_data_from_file

class FileSelection:
    def __init__(self, win, gv, layout):
        self.win = win
        self.gv = gv
        self.layout = layout

        self.name = 'File selection'

        self.file_name = './experiment_csv/2exp_pinch_close_2018-08-29 19:44:54.567417.csv'
        self.name = 'Open file'

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


class PortionGraph:
    def __init__(self, layout):
        self.layout = layout

        self.name = 'Portion graph'


import pyqtgraph as pg

class FullGraph:
    def __init__(self, gv, ch, gr_layout):
        self.ch = ch
        self.gr_layout = gr_layout

        self.name = 'Full graph'

        self.x_range = 8000
        self.N_DATA = len(gv.data_queue[0])

        self.layout, self.gr = self.add_graph()
        self.add_slider()

    def add_graph(self):
        layout = QGridLayout()
        gr = QGroupBox(f'ch {self.ch}')
        gr.setLayout(layout)
        # region = pg.LinearRegionItem()
        plot = pg.PlotWidget()
        plot.setXRange(0, self.x_range)
        layout.addWidget(plot)
        self.gr_layout.addWidget(gr, self.ch, 0)
        return layout, gr

    def add_slider(self):
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, self.N_DATA)
        self.layout.addWidget(self.slider)


