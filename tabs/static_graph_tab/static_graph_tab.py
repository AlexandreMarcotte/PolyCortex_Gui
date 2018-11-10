# -- General packages --
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

        file_selector_gr, portion_graph_gr, full_graph_gr = self.create_grps()
        splitter = self.create_splitter(portion_graph_gr, full_graph_gr)
        scroller = self.create_scroll(splitter)
        self.add_gr_to_main_widget(file_selector_gr, scroller)

        self.tab_w.setLayout(self.tab_w.layout)

    def create_grps(self):
        file_selector = FileSelector('File selector', self.main_window, self.gv)
        left_gr = LeftGraphLayout(
            'Avg classif graph - Portion graph - Classif graph', self.gv)
        right_gr = RightGraphLayout('Full graph', self.gv)
        return file_selector.gr, left_gr.gr, right_gr.gr

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


# -- General packages--
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from functools import partial
# -- My packages --
from app.colors import *
from generate_signal.from_file import read_data_from_file




import pyqtgraph as pg


class Group:
    def create_gr_and_layout(self, name, parent_layout=None, ch=None):
        layout = QGridLayout()
        gr = QGroupBox(name)
        gr.setLayout(layout)
        if parent_layout is not None:
            parent_layout.addWidget(gr, ch, 0)
        return layout, gr


class FileSelector(Group):
    def __init__(self, name, win, gv):
        super().__init__()
        self.name = name
        self.win = win
        self.gv = gv
        # Initialize data lists before reading
        self.data = []
        self.t = []
        self.exp = []
        self.file_name = './experiment_csv/2exp_pinch_close_2018-08-29 19:44:54.567417.csv'

        self.gr, self.path_line_edit = self.init_layout()

    def init_layout(self):
        layout, gr = self.create_gr_and_layout(self.name)
        self.add_choose_file_b(layout)
        path_line_edit = self.add_data_path_line_edit(layout)
        self.add_open_file_b(layout)
        return gr, path_line_edit

    def add_choose_file_b(self, layout):
        b = QtGui.QPushButton('Choose file containing data')
        b.setStyleSheet(f'background-color: {blue_b}')
        b.clicked.connect(partial(self.choose_file))
        layout.addWidget(b, 0, 0)

    def add_data_path_line_edit(self, layout):
        """Create text box to show or enter path to data file"""
        path_line_edit = QtGui.QLineEdit(self.file_name)
        layout.addWidget(path_line_edit, 0, 1)
        return path_line_edit

    def add_open_file_b(self, layout):
        open_file_b = QtGui.QPushButton('Open File')
        open_file_b.clicked.connect(partial(self.read_data))
        layout.addWidget(open_file_b, 0, 2)

    @pyqtSlot()
    def choose_file(self):
        # From: https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        f_name, _ = QFileDialog.getOpenFileName(
            self.win, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        if f_name:
            self.path_line_edit.setText(f_name)
            self.f_name = f_name

    @pyqtSlot()
    def read_data(self):
        self.data, self.t, self.exp = \
            read_data_from_file(self.path_line_edit.text(), n_ch=self.gv.N_CH)


class GraphLayout(Group):
    def __init__(self):
        super().__init__()

    def add_all_graph(self, parent_layout, gv):                                # TODO: ALEXM: find how redefinintion of functions are done
        for ch in range(gv.N_CH):
            layout, gr = self.create_gr_and_layout(
                name=f'ch {ch}', parent_layout=parent_layout, ch=ch)
            self.create_graphs(layout)


class LeftGraphLayout(GraphLayout):
    def __init__(self, name, gv):
        super().__init__()

        parent_layout, self.gr = self.create_gr_and_layout(name)
        self.add_all_graph(parent_layout, gv)

    def create_graphs(self, layout):
        PortionGraph().add_plot(layout, y=0, x=2, x_range=True)
        AvgClassifGraph().add_plot(layout, h=2, w=2)
        ClassifGraph().add_plot(layout, y=1, x=2)


class RightGraphLayout(GraphLayout):
    def __init__(self, name, gv):
        super().__init__()
        self.gv = gv

        parent_layout, self.gr = self.create_gr_and_layout(name)
        self.add_all_graph(parent_layout, gv)
        self.slider = None

    def create_graphs(self, layout):
        full_graph = FullGraph()
        full_graph.add_plot(layout, x_range=8000)
        self.slider = full_graph.add_slider(layout, len(self.gv.data_queue[0]))


class Graph:
    def add_plot(self, layout, y=0, x=0, h=1, w=1, x_range=None):
        plot = pg.PlotWidget()
        if x_range:
            plot.setXRange(0, x_range)
        layout.addWidget(plot, y, x, h, w)
        return plot

    def add_slider(self, layout, N_DATA):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, N_DATA)
        layout.addWidget(slider)
        return slider


class PortionGraph(Graph):
    def __init__(self):
        super().__init__()
class AvgClassifGraph(Graph):
    def __init__(self):
        super().__init__()
class ClassifGraph(Graph):
    def __init__(self):
        super().__init__()
class FullGraph(Graph):
    def __init__(self):
        super().__init__()


