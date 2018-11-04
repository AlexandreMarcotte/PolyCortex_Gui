# Graph the data
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
import pyqtgraph as pg

from functools import partial
import random
import numpy as np
from sklearn.externals import joblib
import matplotlib.pyplot as plt
# My packages
from generated_signal import read_data_from_file
from signal_manipulation import uniformize_data

class StaticGraphTab:
    def __init__(self, main_window, tab_w, gv):
        super().__init__()
        self.main_window = main_window
        self.tab_w = tab_w
        self.gv = gv
        # Stationnary graph
        self.full_graph_x_range = 8000
        self.slider_last = 0
        self.static_graph_file_name = './experiment_csv/2exp_pinch_close_2018-08-29 19:44:54.567417.csv'
        # Brush color for region delimiting experimentation events
        self.pale_red = (255, 0, 0, 35)
        self.red = (255, 0, 0, 50)
        self.green = (0, 255, 0, 50)
        self.blue = (0, 0, 255, 50)
        self.yellow = (255, 255, 0, 50)
        self.purple = (146, 56, 219, 50)
        self.region_brush = [self.red, self.green, self.blue,
                             self.yellow, self.purple]
        # Classification model
        self.clf = joblib.load('linear_svm_fitted_model.pkl')
        self.avg_emg_class_type = np.load('avg_emg_class_type.npy')
        self.classified_data = [[] for _ in range(self.gv.N_CH)]
        self.classified_once_every = 6
        self.classified_pos = 250
        self.emg_signal_len = 170
        # Create the tab itself
        self.create_tab()

    def create_tab(self):
        self.tab_w.layout = QGridLayout(self.main_window)
        # Create two different layout split by a QSplitter
        self.create_layouts()
        # Place things on the two layouts
        self.open_data_from_file()
        # Set the layout
        self.tab_w.setLayout(self.tab_w.layout)

    def create_layouts(self):
        # Create open file layout:
        self.open_file_layout = QGridLayout()
        self.open_file_group = QGroupBox('Open file')
        self.open_file_group.setLayout(self.open_file_layout)
        # Create portion graph layout:
        self.portion_graph_layout = QGridLayout()
        self.portion_graph_group = QGroupBox('Portion graph')
        self.portion_graph_group.setLayout(self.portion_graph_layout)
        # Create full graph layout:
        self.full_graph_layout = QGridLayout()
        self.full_graph_group = QGroupBox('Full graph')
        self.full_graph_group.setLayout(self.full_graph_layout)
        # Create scrolling region for portion graph
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        # Add the electrodes layout split by the Qsplitter
        self.add_splitter_between_layouts()

    def add_splitter_between_layouts(self):
        # Create a splitter for the electrodes
        layout_splitter = QSplitter(Qt.Horizontal)
        layout_splitter.addWidget(self.portion_graph_group)
        layout_splitter.addWidget(self.full_graph_group)
        # Add the spliter to the entire tab
        self.scroll.setWidget(layout_splitter)
        # Add widget to the main layout
        self.tab_w.layout.addWidget(self.open_file_group)
        self.tab_w.layout.addWidget(self.scroll)

    def open_data_from_file(self):
        # Create button to open date file
        chose_file = QtGui.QPushButton('Choose file containing data')
        chose_file.setStyleSheet("background-color: rgba(0, 0, 150, 0.5)")
        chose_file.clicked.connect(partial(self.open_static_data_file))
        row=0; col=0; rowspan=1; colspan=1
        self.open_file_layout.addWidget(chose_file,
                                        row, col, rowspan, colspan)
        # Create text box to show or enter path to data file
        self.data_path = QtGui.QLineEdit(self.static_graph_file_name)
        row=0; col=1; rowspan=1; colspan=1
        self.open_file_layout.addWidget(self.data_path,
                                        row, col, rowspan, colspan)
        # Read the data from the file
        self.open_file_b = QtGui.QPushButton('Open File')
        self.open_file_b.clicked.connect(partial(self.create_stationnary_plot))
        row=0; col=2; rowspan=1; colspan=1
        self.open_file_layout.addWidget(self.open_file_b,
                                        row, col, rowspan, colspan)
        self.add_static_plots()

    @pyqtSlot()
    def open_static_data_file(self):
        # From: https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self.main_window, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            self.data_path.setText(file_name)
            self.static_graph_file_name = file_name

    @pyqtSlot()
    def create_stationnary_plot(self):
        # Read data from file
        data, t, exp = read_data_from_file(self.data_path.text(),
                                                n_ch=self.gv.N_CH)
        N_DATA = len(data[0])

        self.static_portion_graph_update = []
        self.static_classif_graph_update = []
        self.classif_region_updates = []
        self.sliders = []
        self.classif_regions = []
        self.portion_regions = []

        for ch, ch_data in enumerate(data):
            self.pos = 0
            # Portion plot
            self.portion_plots[ch].plot(ch_data, pen='g')
            self.add_all_exp_region_for_this_ch(ch, exp)
            self.add_classif_region(ch)
            # Full plot
            self.all_data_plots[ch].plot(ch_data, pen='w')
            self.add_sliders(ch, N_DATA)
            self.add_sliding_region(ch)
            # Create classification graph and plot
            self.classify_ch_data(ch, ch_data)
            self.classif_plots[ch].plot(self.classified_data[ch], pen='b')

    def classify_ch_data(self, ch, ch_data):
        print('len', len(ch_data))
        ch_data = np.array(ch_data)
        while self.pos+self.emg_signal_len < len(ch_data):
            emg_signal = ch_data[0+self.pos:170+self.pos]
            # If the array is not filled with 0 values
            if emg_signal.any():
                emg_signal = uniformize_data(emg_signal, len(emg_signal))
                class_type = self.clf.predict([emg_signal])[0]
            else:
                class_type = 0
            for _ in range(self.classified_once_every):
                self.classified_data[ch].append(class_type)
            self.pos += self.classified_once_every
        
    def add_sliding_region(self, no):
        """
        Add Sliding region on the graph that will be add where experiment
        events occured during the training
        """
        # Tell the ViewBox to exclude this item when doing auto-range
        # calculations.
        self.all_data_plots[no].addItem(self.regions[no], ignoreBounds=True)
        # Activate ability for the graph to scale the y axis
        self.all_data_plots[no].setAutoVisible(y=True)
        self.portion_plots[no].setAutoVisible(y=True)

        # - - Update the left side based on the right side region and slider pos
        # - Portion graph
        # Create 8 update function object, one for every portion plot
        self.static_portion_graph_update.append(
                StaticGraphUpdate(self.regions[no], self.portion_plots[no]))
        # Connect all the update functions
        self.regions[no].sigRegionChanged.connect(
                self.static_portion_graph_update[no].update_plot_range)
        # - Classification graph
        self.static_classif_graph_update.append(
                StaticGraphUpdate(self.regions[no], self.classif_plots[no]))
        self.regions[no].sigRegionChanged.connect(
                self.static_classif_graph_update[no].update_plot_range)

        # self.portion_plots[no].sigRangeChanged.connect(
        #     self.static_graph_update[no].update_region)

        self.regions[no].setRegion([0, 800])

    def add_sliders(self, ch, N_DATA):
        # # Slider to scoll through all data
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, N_DATA)
        row=ch*2+2; col=0; rowspan=1; colspan=1
        self.full_ch_layouts[ch].addWidget(self.slider,
                                           row, col, rowspan, colspan)
        self.update_slider_graph = UpdateSliderGraph(
                self.slider, self.all_data_plots[ch],
                self.regions[ch], self.slider_last,
                self.classif_regions[ch], self.portion_regions[ch],
                self.classified_pos)
        self.sliders.append(self.update_slider_graph)
        self.slider.valueChanged.connect(self.sliders[ch].update_graph_range)
        
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

    def add_one_exp_region(self, ch, no, val):
        """ Add a pyqtgraph region on one single event occurence """
        region = pg.LinearRegionItem()
        self.portion_plots[ch].addItem(region, ignoreBounds=True)
        region.setRegion([no-60, no+110])
        region.setBrush(self.region_brush[int(val)])

    def add_classif_region(self, ch):
        """
        Add a region on the portion graph that indicate the region that
        was used to calculate the corresponding value on the classification
        graph
        """
        # Portion graph (rectangle up)
        self.portion_regions.append(pg.LinearRegionItem())
        self.portion_plots[ch].addItem(self.portion_regions[ch])
        self.portion_regions[ch].setRegion(
                [self.classified_pos, self.classified_pos+self.emg_signal_len])
        self.portion_regions[ch].setBrush(self.pale_red)
        # Classification graph (line down)
        self.classif_regions.append(pg.LinearRegionItem())
        self.classif_plots[ch].addItem(self.classif_regions[ch])
        self.classif_regions[ch].setRegion(
                [self.classified_pos, self.classified_pos])
        self.classif_regions[ch].setBrush(self.pale_red)
        # Connect the rectangular region in the emg graph to the line shaped
        # one in the classification data graph
        self.classif_region_updates.append(
                ClassifRegionUpdate(self.portion_regions[ch],
                                    self.classif_regions[ch],
                                    self.portion_plots[ch],
                                    self.classified_data[ch],
                                    self.all_char_class_type[ch],
                                    self.avg_classif_curves[ch],
                                    self.avg_emg_class_type))
        # Connect all the update functions
        self.portion_regions[ch].sigRegionChanged.connect(
                self.classif_region_updates[ch].update_pos_and_avg_graph)

    def add_static_plots(self):
        # Regions
        self.regions = []
        # Text list
        self.all_char_class_type = []
        # Plot lists
        self.portion_plots = []
        self.portion_ch_layouts = []
        self.classif_plots = []
        self.all_data_plots = []
        self.avg_classif_plots = []
        self.avg_classif_curves = []
        # Layout
        self.full_ch_layouts = []
        for ch in range(self.gv.N_CH):
            # Portion graph
            self.add_portion_static_plot(ch)
            # Full graph
            self.add_full_static_graph(ch)
    #
    # def assign_n_to_ch(self):
    #     for ch in range(self.gv.N_CH):
    #         # +1 so the number str start at 1
    #         b_on_off_ch = QtGui.QPushButton(str(ch + 1))
    #         style = ("""QPushButton { background-color: rgba(40, 40, 40, 100);
    #                     min-width: 14px}""")
    #         b_on_off_ch.setStyleSheet(style)
    #         # Set position and size of the button values
    #         row=ch*2+1; col=0; rowspan=1
    #         self.portion_graph_layout.addWidget(b_on_off_ch, row, col, rowspan, 1)

    def add_portion_static_plot(self, ch):
        # - Portion
        self.portion_ch_layouts.append(QGridLayout())
        self.portion_ch_group = QGroupBox(f'ch {ch+1}')
        self.portion_ch_group.setLayout(self.portion_ch_layouts[ch])
        # Instanciate the plot containing the crosshair
        self.portion_plots.append(pg.PlotWidget())
        # Instantiate the plot containing the values of classification
        self.classif_plots.append(pg.PlotWidget())
        # Instantiate the average classification
        self.avg_classif_plots.append(pg.PlotWidget())
        # Portion of the graph
        row=ch*2; col=3; rowspan=1; colspan=1
        self.portion_ch_layouts[ch].addWidget(self.portion_plots[ch],
                                              row, col, rowspan, colspan)
        # Classification plot
        row=ch*2+1; col=3; rowspan=1; colspan=1
        self.portion_ch_layouts[ch].addWidget(self.classif_plots[ch],
                                              row, col, rowspan, colspan)
        row=ch*2; col=0; rowspan=2; colspan=3
        self.portion_ch_layouts[ch].addWidget(self.avg_classif_plots[ch],
                                              row, col, rowspan, colspan)
        # Add number of the current classification in the plot's right corner
        self.all_char_class_type.append(pg.TextItem(fill=(0, 0, 0), anchor=(0.5, 0)))
        html = f'0'
        self.all_char_class_type[ch].setHtml(html)
        self.all_char_class_type[ch].setPos(1, 1)
        self.avg_classif_plots[ch].addItem(self.all_char_class_type[ch])
        self.avg_classif_plots[ch].setXRange(0, self.emg_signal_len)
        self.avg_classif_plots[ch].setYRange(-1, 1)
        self.avg_classif_curves.append(
                    self.avg_classif_plots[ch].plot(np.zeros(self.emg_signal_len)))

        # Add the group to the left side of the separation
        self.portion_graph_layout.addWidget(self.portion_ch_group)

    def add_full_static_graph(self, ch):
        # Full graph
        self.full_ch_layouts.append(QGridLayout())
        self.full_graph_ch_group = QGroupBox(f'ch {ch+1}')
        self.full_graph_ch_group.setLayout(self.full_ch_layouts[ch])

        # Region of selection in the 'all_data_plot'
        self.regions.append(pg.LinearRegionItem())

        # Instanciate the plot containing all the data
        self.all_data_plots.append(pg.PlotWidget())
        self.all_data_plots[ch].setXRange(0, self.full_graph_x_range)

        # All the values open from the saved file
        row=ch*2+1; col=0; rowspan=1; colspan=1
        self.full_ch_layouts[ch].addWidget(self.all_data_plots[ch],
                                           row, col, rowspan, colspan)
        # Add these group by channel to the right side of the separation
        self.full_graph_layout.addWidget(self.full_graph_ch_group)


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
        self.all_data_plot.setXRange(v, v+10000)
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

