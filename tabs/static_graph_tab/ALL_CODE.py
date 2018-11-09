# -- General packages --
# Graph
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
import pyqtgraph as pg

import numpy as np
from sklearn.externals import joblib
import os
# -- My packages --
from generate_signal.from_file import read_data_from_file
from app.colors import *
from .static_graph_update import StaticGraphUpdate
from .file_group import FileGroup
from .update_slider_graph import UpdateSliderGraph
from .full_graph import FullGraph
from .portion_graph import PortionGraph


class StaticGraphTab:
    def __init__(self, main_window, tab_w, gv):
        # self.main_window = main_window
        # self.tab_w = tab_w
        # self.gv = gv
        # Stationnary graph
        self.slider_last = 0

        # Classification model
        clf_path = 'machine_learning/linear_svm_fitted_model.pkl'
        self.clf = joblib.load(os.path.join(os.getcwd(), clf_path))
        avg_emg_path = 'tabs/static_graph_tab/avg_emg_class_type.npy'
        self.avg_emg_class_type = np.load(os.path.join(os.getcwd(), avg_emg_path))
        self.classified_data = [[] for _ in range(self.gv.N_CH)]
        self.classified_once_every = 1000
        self.classified_pos = 250
        self.emg_signal_len = 170
        # Create the tab itself
        self.create_tab()

    def create_tab(self):
        self.tab_w.layout = QGridLayout(self.main_window)
        # Open file group
        open_file = FileGroup(self.main_window, self.static_graph_file_name,
                              self.create_stationnary_plot)
        self.path_line_edit = open_file.path_line_edit

        # Portion graph group
        portion_graph_group = self.create_portion_graph()


        # full_graph_group = self.create_full_graph()                          # improve the code damnn
        self.full_graph = FullGraph()                  # Improve this portion of the code
        full_graph_group = self.full_graph.group_box
        layout_splitter = self.create_layout_splitter(full_graph_group,
                                                      portion_graph_group)
        # scroll = self.create_scroll(layout_splitter)
        # self.add_group_to_main_widget(open_file.group, scroll)
        # self.add_static_plots()

        # Set the layout
        # self.tab_w.setLayout(self.tab_w.layout)

    # def create_portion_graph(self):
    #     self.portion_graph_layout = QGridLayout()
    #     portion_graph_group = QGroupBox('Portion graph')
    #     portion_graph_group.setLayout(self.portion_graph_layout)
    #     return portion_graph_group

    # def create_scroll(self, layout_splitter):
    #     scroll = QScrollArea()
    #     scroll.setWidgetResizable(True)
    #     scroll.setWidget(layout_splitter)
    #     return scroll

    # def add_group_to_main_widget(self, open_file_group, scroll):
    #     self.tab_w.layout.addWidget(open_file_group)
    #     self.tab_w.layout.addWidget(scroll)

    # def add_static_plots(self):
        # # Text list
        # self.all_char_class_type = []
        # # Plot lists
        # self.portion_plots = []
        # self.classif_plots = []
        # self.avg_classif_plots = []
        # self.avg_classif_curves = []

        for ch in range(self.gv.N_CH):
            # Portion graph
            self.add_portion_static_plot(ch)
            # Full graph
            self.full_graph.add_full_static_graph(ch)                          # improve the code damnn
            self.all_data_plots = self.full_graph.plots
            self.regions = self.full_graph.regions
            # self.add_full_static_graph(ch)

    # @pyqtSlot()
    # def create_stationnary_plot(self):
    #     # Read data from file
    #     data, t, exp = read_data_from_file(self.path_line_edit.text(),
    #                                        n_ch=self.gv.N_CH)
        N_DATA = len(data[0])

        # self.static_portion_graph_update = []
        # self.static_classif_graph_update = []
        # self.classif_region_updates = []
        # self.classif_regions = []
        # self.portion_regions = []

        for ch, ch_data in enumerate(data):
            self.pos = 0
            # Portion plot



            # Full plot
            self.full_graph.add_sliders(ch, N_DATA)                            # improve
            self.slider = self.full_graph.slider

            self.update_slider_graph = UpdateSliderGraph(
                self.slider, self.all_data_plots[ch], self.regions[ch],
                self.slider_last, self.classif_regions[ch],
                self.portion_regions[ch], self.classified_pos)

            self.all_data_plots[ch].plot(ch_data, pen='w')
            self.full_graph.connect_slider(ch, self.update_slider_graph)
            # self.add_sliders(ch, N_DATA)                                       # improve the code
            self.add_sliding_region(ch)
            self.full_graph.add_sliding_region(ch)  # improve

            # Create classification graph and plot
            self.classify_ch_data(ch, ch_data)
            self.classif_plots[ch].plot(self.classified_data[ch], pen='b')


# -- General packages --
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
# -- My packages --
from app.colors import *
from data_processing_pipeline.uniformize_data import uniformize_data
from .classif_region_update import ClassifRegionUpdate


class PortionPlotsLayout:
    def __init__(self):
        self.portion_ch_layouts = []
        # Brush color for region delimiting experimentation events
        self.region_brush = [red, green, blue, yellow, purple]

    # def create_all_ch_layout(self):
    #     self.portion_ch_layouts.append(QGridLayout())
    #     portion_ch_group = QGroupBox(f'ch {ch+1}')
    #     portion_ch_group.setLayout(self.portion_ch_layouts[ch])

    def complete_layout(self):
        """Once the group is completed add it to the left side of
           the separation"""
        self.portion_graph_layout.addWidget(portion_ch_group)


class PortionGraph:
    def __init__(self, emg_signal_len):
        self.emg_signal_len = emg_signal_len

        self.portion_ch_layouts = []
        # Text list
        self.all_char_class_type = []
        # Plot lists
        self.portion_plots = []
        self.classif_regions = []
        self.portion_regions = []

        self.static_portion_graph_update = []
        self.static_classif_graph_update = []
        self.classif_region_updates = []

        self.classified_pos = 250

        self.portion_graph_group = self.create_portion_plot()

    def create_portion_plot(self, ch):
        """Instantiating the plot containing the portion of the full plot
           that is located on the righ side"""
        self.portion_plots.append(pg.PlotWidget())
        self.portion_ch_layouts[ch].addWidget(self.portion_plots[ch], ch * 2, 3)

    def add_one_exp_region(self, ch, no, val):
        """ Add a pyqtgraph region on a single event """
        region = pg.LinearRegionItem()
        self.portion_plots[ch].addItem(region, ignoreBounds=True)
        region.setRegion([no - 60, no + 110])
        region.setBrush(self.region_brush[int(val)])

    def add_all_exp_region_for_this_ch(self, ch, exp):
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
                    print('val', val, ch)
                    self.add_one_exp_region(ch, no, val)
                elif (val == 3 or val == 4) and (ch == 2 or ch == 3):
                    self.add_one_exp_region(ch, no, val)

    def add_classif_region(self, ch):
        """Add a region on the portion graph that indicate the region that
           was used to calculate the corresponding value on the classification
           graph"""

        self.portion_regions.append(pg.LinearRegionItem())
        self.portion_plots[ch].addItem(self.portion_regions[ch])
        self.portion_regions[ch].setRegion(
            [self.classified_pos, self.classified_pos + self.emg_signal_len])
        self.portion_regions[ch].setBrush(pale_red)
        # Connect the rectangular region in the emg graph to the line shaped
        # one in the classification data graph
        self.classif_region_updates.append(
            ClassifRegionUpdate(
                self.portion_regions[ch], self.classif_regions[ch],
                self.portion_plots[ch], self.classified_data[ch],
                self.all_char_class_type[ch], self.avg_classif_curves[ch],
                self.avg_emg_class_type))
        # Connect all the update functions
        self.portion_regions[ch].sigRegionChanged.connect(
            self.classif_region_updates[ch].update_pos_and_avg_graph)

    def classify_ch_data(self, ch, ch_data):
        print('len', len(ch_data))
        ch_data = np.array(ch_data)
        while self.pos + self.emg_signal_len < len(ch_data):
            emg_signal = ch_data[0 + self.pos:170 + self.pos]
            # If the array is not filled with 0 values
            if emg_signal.any():
                emg_signal = uniformize_data(emg_signal, len(emg_signal))
                class_type = self.clf.predict([emg_signal])[0]
            else:
                class_type = 0
            for _ in range(self.classified_once_every):
                self.classified_data[ch].append(class_type)
            self.pos += self.classified_once_every


import pyqtgraph as pg


class ClassifGraph:
    def __init__(self):
        pass

    def create_classif_plot(self, ch):
        """Instantiate the plot containing the values of classification"""
        self.classif_plots.append(pg.PlotWidget())
        self.portion_ch_layouts[ch].addWidget(self.avg_classif_plots[ch], ch * 2, 0, 2, 3)

    def add_classif_regions(self):
        self.classif_regions.append(pg.LinearRegionItem())
        self.classif_plots[ch].addItem(self.classif_regions[ch])
        self.classif_regions[ch].setRegion(
            [self.classified_pos, self.classified_pos])
        self.classif_regions[ch].setBrush(pale_red)



class ClassifRegionUpdate:
    def __init__(self, portion_region, classif_region, plot, classified_data,
                 char_class_type, avg_classif_curve, avg_emg_class_type):
        self.portion_region = portion_region
        self.classif_region = classif_region
        self.plot = plot
        self.classified_data = classified_data
        self.char_class_type = char_class_type
        self.avg_classif_curve = avg_classif_curve
        self.avg_emg_class_type = avg_emg_class_type

    def update_pos_and_avg_graph(self):
        # Update the average classification grap (complete left)
        r_left = self.portion_region.boundingRect().left()
        # r_right = self.portion_region.boundingRect().right()
        try:
            classified_type = self.classified_data[int(r_left)]
            html = f'{classified_type}'
            self.char_class_type.setHtml(html)
            self.avg_classif_curve.setData(self.avg_emg_class_type[classified_type])
            self.classif_region.setRegion([r_left, r_left])
        except IndexError as e:
            print(e)

# # -- General packages
# from PyQt5.QtCore import pyqtSlot
# from PyQt5.QtWidgets import *
# from PyQt5 import QtGui
# from functools import partial
# # -- My packages --
# from app.colors import *
#

# class FileGroup:
#     def __init__(self, main_win, file_name, create_stationnary_plot):
#         # self.main_win = main_win
#         # self.file_name = file_name
#         self.create_stationnary_plot = create_stationnary_plot
#
#         self.path_line_edit = None
#         self.layout, self.group = self.create_open_file()
#         self.create_open_data_from_file_layout(self.layout)

    # def create_open_file(self):
    #     layout = QGridLayout()
    #     group = QGroupBox('Open file')
    #     group.setLayout(layout)
    #     return layout, group

    # def create_open_data_from_file_layout(self, layout):
    #     self.add_choose_file_btn(layout)
    #     self.add_data_path_line_edit(layout)
    #     self.add_open_file_b(layout)
    #
    # def add_choose_file_btn(self, layout):
    #     chose_file_b = QtGui.QPushButton('Choose file containing data')
    #     chose_file_b.setStyleSheet(f'background-color: {blue_b}')
    #     chose_file_b.clicked.connect(partial(self.open_static_data_file))
    #     layout.addWidget(chose_file_b, 0, 0)
    #
    # def add_data_path_line_edit(self, layout):
    #     """Create text box to show or enter path to data file"""
    #     self.path_line_edit = QtGui.QLineEdit(self.file_name)
    #     layout.addWidget(self.path_line_edit, 0, 1)
    #
    # def add_open_file_b(self, layout):
    #     open_file_b = QtGui.QPushButton('Open File')
    #     open_file_b.clicked.connect(partial(self.create_stationnary_plot))
    #     layout.addWidget(open_file_b, 0, 2)
    #
    # @pyqtSlot()
    # def open_static_data_file(self):
    #     # From: https://pythonspot.com/pyqt5-file-dialog/
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.DontUseNativeDialog
    #     file_name, _ = QFileDialog.getOpenFileName(
    #         self.main_win, "QFileDialog.getOpenFileName()", "",
    #         "All Files (*);;Python Files (*.py)", options=options)
    #     if file_name:
    #         self.path_line_edit.setText(file_name)
    #         self.file_name = file_name

from PyQt5.QtWidgets import *
import pyqtgraph as pg
from PyQt5.QtCore import Qt


class FullGraph:
    def __init__(self):
        self.regions = []
        self.layouts = []
        self.plots = []
        self.sliders = []
        # self.x_range = 8000

        self.group_box, self.layout = self.create_group_and_layout()

    # def create_group_and_layout(self):
    #     layout = QGridLayout()
    #     group_box = QGroupBox('Full graph')
    #     group_box.setLayout(layout)
    #     return group_box, layout

    # def add_full_static_graph(self, ch):
    #     # Full graph
    #     self.layouts.append(QGridLayout())
    #     self.graph_group = QGroupBox(f'ch {ch+1}')
    #     self.graph_group.setLayout(self.layouts[ch])
    #     # Region of selection in the 'all_data_plot'
    #     self.regions.append(pg.LinearRegionItem())
    #     # Instanciate the plot containing all the data
    #     self.plots.append(pg.PlotWidget())
    #     self.plots[ch].setXRange(0, self.x_range)
    #     # All the values open from the saved file
    #     self.layouts[ch].addWidget(self.plots[ch], ch*2+1, 0)
    #     # Add these group by channel to the right side of the separation
    #     self.layout.addWidget(self.graph_group)
    #
    # def add_sliders(self, ch, N_DATA):
    #     # # Slider to scoll through all data
    #     self.slider = QSlider(Qt.Horizontal)
    #     self.slider.setRange(0, N_DATA)
    #     self.layouts[ch].addWidget(self.slider, ch*2+2, 0)

    def connect_slider(self, ch, update_slider_graph):
        self.sliders.append(update_slider_graph)
        self.slider.valueChanged.connect(self.sliders[ch].update_graph_range)

    def add_sliding_region(self, no):
        """ Add Sliding region on the graph that will be add where
            experiment events occured during the training
        """
        self.plots[no].addItem(self.regions[no], ignoreBounds=True)
        # Activate ability for the graph to scale the y axis
        self.plots[no].setAutoVisible(y=True)


    def add_sliding_region(self, ch):
        """
        Add Sliding region on the graph that will be add where experiment
        events occured during the training
        """
        self.portion_plots[ch].setAutoVisible(y=True)
        # - - Update the left side based on the right side region and slider pos
        # - Portion graph
        # Create 8 update function object, one for every portion plot
        self.static_portion_graph_update.append(
            StaticGraphUpdate(self.regions[ch], self.portion_plots[ch]))
        # Connect all the update functions
        self.regions[ch].sigRegionChanged.connect(
            self.static_portion_graph_update[ch].update_plot_range)
        # - Classification graph
        self.static_classif_graph_update.append(
            StaticGraphUpdate(self.regions[ch], self.classif_plots[ch]))
        self.regions[ch].sigRegionChanged.connect(
            self.static_classif_graph_update[ch].update_plot_range)

        self.regions[ch].setRegion([0, 800])



class StaticGraphUpdate:
    def __init__(self, region, plot):
        self.region = region
        self.plot = plot

    def update_plot_range(self):
        """
        Update the portion plot (top left) range based on the region position
        on the full graph (right)
        """
        minX, maxX = self.region.getRegion()
        self.plot.setXRange(minX, maxX, padding=0)



class UpdateSliderGraph:
    """
    Update the position X range of the full graph on the right side based
    on the position of the slider. The portion rectangle that is contained in
    this graph is updated at the same time
    """

    def __init__(self, slider, all_data_plot, region, slider_last,
                 classif_region, portion_region, classified_pos):
        self.slider = slider
        self.all_data_plot = all_data_plot
        self.region = region
        self.slider_last = slider_last
        self.classif_region = classif_region
        self.portion_region = portion_region
        self.classified_pos = classified_pos

    def update_graph_range(self):
        v = self.slider.value()
        # Keep track of the movement of the slider between two updates
        delta_slider = v - self.slider_last
        self.slider_last = v
        # Update the graph range based on the slider position
        self.all_data_plot.setXRange(v, v + 10000)
        r_right = self.region.boundingRect().right()
        r_left = self.region.boundingRect().left()
        # Update the region position based on the delta position of the slider
        self.region.setRegion([r_right + delta_slider,
                               r_left + delta_slider])

        # Classif region
        r_right = self.classif_region.boundingRect().right()
        r_left = self.classif_region.boundingRect().left()
        # Update the region position based on the delta position of the slider
        self.classif_region.setRegion([r_right + delta_slider,
                                       r_left + delta_slider])
        # Portion region
        r_right = self.portion_region.boundingRect().right()
        r_left = self.portion_region.boundingRect().left()
        # Update the region position based on the delta position of the slider
        self.portion_region.setRegion([r_right + delta_slider,
                                       r_left + delta_slider])