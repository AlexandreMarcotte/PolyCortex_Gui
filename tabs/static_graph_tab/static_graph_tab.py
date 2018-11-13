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
        updater = Updater()
        updater.connect_all(right_panel, left_panel, self.gv)


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
            read_data_from_file(self.path_line_edit.text(), n_ch=self.gv.N_CH)   # clean this part
        for ch in range(self.gv.N_CH):
            # Right panel
            self.right_gr.full_graphs[ch].plot_data(data[ch], color='w')
            self.right_gr.sliders[ch].setMaximum(len(data[0]))
            # Left panel
            self.left_gr.portion_graphs[ch].plot_data(data[ch], color='g')
            self.left_gr.portion_graphs[ch].add_all_experimentation_regions(ch, exp)
            classified_data = self.left_gr.classif_graphs[ch].classify_data(data[ch])
            self.left_gr.classif_graphs[ch].plot_data(classified_data, color='b')

            self.left_gr.avg_classif_graphs[ch].plot_data(np.zeros(170), color='w')
            self.left_gr.avg_classif_graphs[ch].classified_data = classified_data
            self.left_gr.avg_classif_graphs[ch].update_pos_and_avg_graph(0)


class LeftGraphLayout(Group):
    def __init__(self, gv, right_panel):
        super().__init__()
        self.gv = gv
        right_panel = right_panel
        self.r_left = right_panel.full_graphs[0].region.boundingRect().left()

        self.portion_graphs = []
        self.classif_graphs = []
        self.avg_classif_graphs = []

        self.x_range = 2000
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
        self.create_classif_graph(layout)

    def create_classif_graph(self, layout):
        avg_classif_graph = AvgClassifGraph()
        avg_classif_graph.add_plot(layout, h=2, w=2, x_range=170)
        self.avg_classif_graphs.append(avg_classif_graph)
        classif_graph = ClassifGraph(self.gv)
        classif_graph.add_plot(layout, y=1, x=2, x_range=self.x_range)
        classif_graph.add_region([self.r_left, self.r_left], yellow)
        self.classif_graphs.append(classif_graph)

    def create_portion_graph(self, layout):
        portion_graph = PortionGraph()
        portion_graph.add_plot(layout, y=0, x=2, x_range=self.x_range)
        # Put the classification region inside the full graph region
        portion_graph.add_region(
            [self.r_left, self.r_left + self.gv.emg_signal_len], pale_red)
        portion_graph.classif_region = portion_graph.region
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
                name=f'', parent_layout=parent_layout, ch=ch)
            self.create_graphs(layout)

    def create_graphs(self, layout):
        full_graph = FullGraph()
        full_graph.add_plot(layout)
        full_graph.add_region(bounds=[0, 1500])
        slider = full_graph.add_slider(layout, 10000)
        self.sliders.append(slider)
        self.full_graphs.append(full_graph)


class Graph:
    def __init__(self):
        self.plot = pg.PlotWidget()
        self.curve = None

    def add_plot(self, layout, y=0, x=0, h=1, w=1, x_range=10000,
                 hide_axis=False):
        if x_range:
            self.plot.setXRange(0, x_range)
        if hide_axis:
            self.plot.plotItem.hideAxis('bottom')

        layout.addWidget(self.plot, y, x, h, w)

    def plot_data(self, data, color):
        self.curve = self.plot.plot(data, pen=color)
        self.plot.setAutoVisible(y=True)

    def add_region(self, bounds, brush_color=blue, movable=True):
        """ Add a pyqtgraph region on a single event """
        self.region = pg.LinearRegionItem(movable=movable)
        self.region.setRegion(bounds)
        self.region.start_pos = bounds[0]
        self.region.last_pos = bounds[0]
        self.plot.addItem(self.region, ignoreBounds=True)
        self.region.setBrush(brush_color)


class PortionGraph(Graph):
    def __init__(self):
        super().__init__()

        self.brushes = [red, green, blue, yellow, purple]

    def add_all_experimentation_regions(self, ch, exp):
        """
        Add a sliding region over the place on the graph where an
        experiment value as occure (ie there is a value for experiment type
        different than 0
        """
        # Add a colored region on the plot where an event as occured
        for no, val in enumerate(exp):
            val = int(val)
            if val:
                if (val == 1 or val == 2) and (ch == 0 or ch == 1):
                    self.add_region(
                        [no - 60, no + 110], brush_color=self.brushes[int(val)],
                        movable=False)
                elif (val == 3 or val == 4) and (ch == 2 or ch == 3):
                    self.add_region(
                        [no - 60, no + 110], brush_color=self.brushes[int(val)],
                        movable=False)

import numpy as np
import os
from sklearn.externals import joblib


class AvgClassifGraph(Graph):
    def __init__(self):
        super().__init__()

        self.num = pg.TextItem(anchor=(0, 0), fill=(0, 0, 0, 0))
        self.classif_type = 0
        avg_emg_path = 'tabs/static_graph_tab/avg_emg_class_type.npy'
        self.avg_emg_class_type = np.load(os.path.join(os.getcwd(), avg_emg_path))
        self.classified_data = None

    def update_pos_and_avg_graph(self, classif_region_pos):
        self.add_classif_class_number()
        try:
            classified_type = self.classified_data[int(classif_region_pos)]
            self.num.setHtml(str(classified_type))
            self.curve.setData(self.avg_emg_class_type[classified_type])
        except IndexError as e:
            print(e)

    def add_classif_class_number(self):
        html = f'{self.classif_type}'
        self.num.setHtml(html)
        self.num.setPos(0, 0.5)
        self.plot.addItem(self.num)


from data_processing_pipeline.uniformize_data import uniformize_data


class ClassifGraph(Graph):
    def __init__(self, gv):
        super().__init__()
        self.gv = gv

        clf_path = 'machine_learning/linear_svm_fitted_model.pkl'
        self.clf = joblib.load(os.path.join(os.getcwd(), clf_path))
        self.classif_interval = 200

    def classify_data(self, data):
        classified_data = []
        data = np.array(data)
        pos = 0
        # While we haven't reach the end of the data
        while pos + self.gv.emg_signal_len < len(data):
            d = data[0 + pos:self.gv.emg_signal_len + pos]
            # If the array is not filled with only 0 values
            if d.any():
                d = uniformize_data(d, len(d))
                classif_value = self.clf.predict([d])[0]
            else:
                classif_value= 0
            # set all the same type for all the interval of classification
            for _ in range(self.classif_interval):
                classified_data.append(classif_value)
            # Update pos for next classification of the type of the signal
            pos += self.classif_interval
        return classified_data


class FullGraph(Graph):
    def __init__(self):
        super().__init__()

        self.region = None
        self.x_range = 10000

    def add_slider(self, layout, N_DATA):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, N_DATA)
        layout.addWidget(slider)
        return slider


class Updater:
    def connect_all(self, right_panel, left_panel, gv):
        sliders = right_panel.sliders
        full_graphs = right_panel.full_graphs
        portion_graphs = left_panel.portion_graphs
        classif_graphs = left_panel.classif_graphs
        avg_classif_graphs = left_panel.avg_classif_graphs

        for ch in range(gv.N_CH):
            self.connect_slider(sliders[ch], full_graphs[ch])
            self.connect_full_graph_region(
                full_graphs[ch], portion_graphs[ch], classif_graphs[ch])
            self.connect_classif_region(
                portion_graphs[ch], classif_graphs[ch], avg_classif_graphs[ch])

    def connect_slider(self, slider, full_graph):
        slider.last_pos = 0
        slider.valueChanged.connect(
            partial(self.slider_update, slider, full_graph))

    def connect_full_graph_region(self, full_graph, portion_graph, classif_graph):
        full_graph.region.sigRegionChanged.connect(
            partial(self.full_graph_region_update,
                    full_graph, portion_graph, classif_graph))

    def connect_classif_region(
            self, portion_graph, classif_graph, avg_classif_graph):
        portion_graph.region.sigRegionChanged.connect(
            partial(self.update_region_w_region,
                portion_graph.region, classif_graph.region, avg_classif_graph,
                    classif_graph))

    def slider_update(self, slider, full_graph):
        self.find_slider_pos(slider)
        self.update_region_w_slider(full_graph.region)
        self.update_plot_range_w_slider(full_graph.plot, full_graph.x_range)

    def full_graph_region_update(self, full_graph, portion_graph, classif_graph):
        self.find_region_pos(full_graph.region)
        self.update_region_w_delta_region(portion_graph.classif_region)
        self.update_plot_range_w_region(full_graph.region, classif_graph.plot)
        self.update_plot_range_w_region(full_graph.region, portion_graph.plot)

    def find_slider_pos(self, slider):
        self.slider_pos = slider.value()
        # Keep track of the movement of the slider between two updates
        self.delta_slider = self.slider_pos - slider.last_pos
        slider.last_pos = self.slider_pos

    def find_region_pos(self, region):
        region.start_pos, _ = region.getRegion()
        self.delta_region = region.start_pos - region.last_pos
        region.last_pos = region.start_pos

    def find_full_graph_region_pos(self, region):
        self.x_min, _ = region.getRegion()
        self.delta_region = self.x_min - region.last_pos

    def update_region_w_delta_region(self, region_follow):
        r_right, r_left = region_follow.getRegion()
        region_follow.setRegion(
            [r_right + self.delta_region, r_left + self.delta_region])

    def update_region_w_region(
            self, region_dictate, region_follow, avg_classif_graph, classif_graph):
        r_right, _ = region_dictate.getRegion()
        region_follow.setRegion([r_right, r_right])
        if avg_classif_graph.classified_data:
            avg_classif_graph.update_pos_and_avg_graph(
                classif_graph.region.getRegion()[0])

    def update_region_w_slider(self, region):
        r_right = region.boundingRect().right()
        r_left = region.boundingRect().left()
        # Update the region position based on the delta position of the slider
        region.setRegion([r_right + self.delta_slider, r_left + self.delta_slider])

    def update_plot_range_w_slider(self, plot, x_range):
        # Update the graph range based on the slider position
        plot.setXRange(self.slider_pos, self.slider_pos + x_range)

    def update_plot_range_w_region(self, region, plot):
        """ Update the portion plot (top left) range based on the region position
           on the full graph (right)
        """
        min_x, max_x = region.getRegion()
        plot.setXRange(min_x, max_x, padding=0)

