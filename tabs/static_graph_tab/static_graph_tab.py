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

        file_selector, left_panel, right_panel = self.create_grps()
        splitter = self.create_splitter(left_panel.gr, right_panel.gr)
        scroller = self.create_scroll(splitter)
        self.add_gr_to_main_widget(file_selector.gr, scroller)

        self.tab_w.setLayout(self.tab_w.layout)

        self.connect_updates(right_panel)

    def create_grps(self):
        left_panel = LeftGraphLayout(self.gv)
        right_panel = RightGraphLayout(self.gv)
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

    def connect_updates(self, right_panel):
        updater = Updater()
        updater.connect_sliders(right_panel.sliders,
                                right_panel.full_graphs)


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
    def __init__(self, name, win, gv, right_gr, left_gr):
        super().__init__()
        self.name = name
        self.win = win
        self.gv = gv
        self.right_gr = right_gr
        self.left_gr = left_gr
        # Initialize data lists before reading                                 TODO: ALEXM: create a panda dataframe instead
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
        data, t, exp = \
            read_data_from_file(self.path_line_edit.text(), n_ch=self.gv.N_CH)
        for ch in range(self.gv.N_CH):
            self.right_gr.full_graphs[ch].plot_data(data[ch])
            self.left_gr.portion_graphs[ch].plot_data(data[ch])
            self.right_gr.sliders[ch].setMaximum(len(data[0]))


class LeftGraphLayout(Group):
    def __init__(self, gv):
        super().__init__()

        self.portion_graphs = []
        self.classif_graphs = []
        self.avg_classif_graphs = []

        name = 'Avg classif graph - Portion graph - Classif graph'
        parent_layout, self.gr = self.create_gr_and_layout(name)
        self.add_all_graph(parent_layout, gv)

    def add_all_graph(self, parent_layout, gv):                                # TODO: ALEXM: find how redefinintion of functions are done
        for ch in range(gv.N_CH):
            layout, gr = self.create_gr_and_layout(
                name=f'ch {ch + 1}', parent_layout=parent_layout, ch=ch)
            self.create_graphs(layout)

    def create_graphs(self, layout):
        self.create_portion_graph(layout)
        AvgClassifGraph().add_plot(layout, h=2, w=2)
        ClassifGraph().add_plot(layout, y=1, x=2)

    def create_portion_graph(self, layout):
        portion_graph = PortionGraph()
        portion_graph.add_plot(layout, y=0, x=2, x_range=True)
        self.portion_graphs.append(portion_graph)


class RightGraphLayout(Group):
    def __init__(self, gv):
        super().__init__()

        self.full_graphs = []
        self.sliders = []

        parent_layout, self.gr = self.create_gr_and_layout('Portion graph')
        self.add_all_graph(parent_layout, gv)


    def add_all_graph(self, parent_layout, gv):                                # TODO: ALEXM: find how redefinintion of functions are done
        for ch in range(gv.N_CH):
            layout, gr = self.create_gr_and_layout(
                name=f'ch {ch + 1}', parent_layout=parent_layout, ch=ch)
            self.create_graphs(layout, gv)

    def create_graphs(self, layout, gv):
        full_graph = FullGraph()
        full_graph.add_plot(layout, x_range=8000)
        slider = full_graph.add_slider(layout, 10)
        self.sliders.append(slider)
        self.full_graphs.append(full_graph)


class Graph:
    def __init__(self):
        self.plot = pg.PlotWidget()

    def add_plot(self, layout, y=0, x=0, h=1, w=1, x_range=None):
        if x_range:
            self.plot.setXRange(0, x_range)
        layout.addWidget(self.plot, y, x, h, w)

    def add_slider(self, layout, N_DATA):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, N_DATA)
        layout.addWidget(slider)
        return slider


class PortionGraph(Graph):
    def __init__(self):
        super().__init__()
    def plot_data(self, data):
        self.plot.plot(data, pen='g')

class AvgClassifGraph(Graph):
    def __init__(self):
        super().__init__()

class ClassifGraph(Graph):
    def __init__(self):
        super().__init__()

class FullGraph(Graph):
    def __init__(self):
        super().__init__()

    def plot_data(self, data):
        self.plot.plot(data, pen='w')


class Updater:
    def __init__(self):

        self.slider_last = 0

    def connect_sliders(self, sliders, full_graphs):
        for slider, full_graph in zip(sliders, full_graphs):
            slider.valueChanged.connect(partial(self.update_graph_range,
                                                slider, full_graph.plot))

    def update_graph_range(self, slider, plot):
        v = slider.value()
        # Keep track of the movement of the slider between two updates
        delta_slider = v - self.slider_last
        self.slider_last = v
        # Update the graph range based on the slider position
        plot.setXRange(v, v + 10000)






