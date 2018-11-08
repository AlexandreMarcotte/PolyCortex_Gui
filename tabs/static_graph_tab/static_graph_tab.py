# Graph the data
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
import pyqtgraph as pg

import numpy as np
from sklearn.externals import joblib
import os
# My packages
from generate_signal.from_file import read_data_from_file
from data_processing_pipeline.uniformize_data import uniformize_data
from app.colors import *
from .static_graph_update import StaticGraphUpdate
from .file_group import FileGroup
from .classif_region_update import ClassifRegionUpdate
from .update_slider_graph import UpdateSliderGraph
from .full_graph import FullGraph


class StaticGraphTab:
    def __init__(self, main_window, tab_w, gv):
        self.main_window = main_window
        self.tab_w = tab_w
        self.gv = gv
        # Stationnary graph
        self.slider_last = 0
        self.static_graph_file_name = './experiment_csv/2exp_pinch_close_2018-08-29 19:44:54.567417.csv'
        # Brush color for region delimiting experimentation events
        self.region_brush = [red, green, blue, yellow, purple]
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

        open_file = FileGroup(self.main_window, self.static_graph_file_name,
                              self.create_stationnary_plot)
        self.data_path = open_file.data_path

        portion_graph_group = self.create_portion_graph()
        # full_graph_group = self.create_full_graph()                          # improve the code damnn
        self.full_graph = FullGraph()                  # Improve this portion of the code
        full_graph_group = self.full_graph.group_box
        layout_splitter = self.create_layout_splitter(full_graph_group,
                                                      portion_graph_group)
        scroll = self.create_scroll(layout_splitter)
        self.add_group_to_main_widget(open_file.open_file_group, scroll)
        self.add_static_plots()

        # Set the layout
        self.tab_w.setLayout(self.tab_w.layout)

    def create_portion_graph(self):
        self.portion_graph_layout = QGridLayout()
        portion_graph_group = QGroupBox('Portion graph')
        portion_graph_group.setLayout(self.portion_graph_layout)
        return portion_graph_group

    def create_layout_splitter(self, full_graph_group, portion_graph_group):
        layout_splitter = QSplitter(Qt.Horizontal)
        layout_splitter.addWidget(portion_graph_group)
        layout_splitter.addWidget(full_graph_group)
        return layout_splitter

    def create_scroll(self, layout_splitter):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(layout_splitter)
        return scroll

    def add_group_to_main_widget(self, open_file_group, scroll):
        self.tab_w.layout.addWidget(open_file_group)
        self.tab_w.layout.addWidget(scroll)

    def add_static_plots(self):
        # Text list
        self.all_char_class_type = []
        # Plot lists
        self.portion_plots = []
        self.portion_ch_layouts = []
        self.classif_plots = []
        self.avg_classif_plots = []
        self.avg_classif_curves = []

        for ch in range(self.gv.N_CH):
            # Portion graph
            self.add_portion_static_plot(ch)
            # Full graph
            self.full_graph.add_full_static_graph(ch)                          # improve the code damnn
            self.all_data_plots = self.full_graph.plots
            self.regions = self.full_graph.regions
            # self.add_full_static_graph(ch)

    @pyqtSlot()
    def create_stationnary_plot(self):
        # Read data from file
        data, t, exp = read_data_from_file(self.data_path.text(),
                                           n_ch=self.gv.N_CH)
        N_DATA = len(data[0])

        self.static_portion_graph_update = []
        self.static_classif_graph_update = []
        self.classif_region_updates = []
        self.classif_regions = []
        self.portion_regions = []

        for ch, ch_data in enumerate(data):
            self.pos = 0
            # Portion plot
            self.portion_plots[ch].plot(ch_data, pen='g')
            self.add_all_exp_region_for_this_ch(ch, exp)
            self.add_classif_region(ch)
            # Full plot
            self.full_graph.add_sliders(ch, N_DATA)  # improve
            self.slider = self.full_graph.slider

            self.update_slider_graph = UpdateSliderGraph(
                self.slider, self.all_data_plots[ch], self.regions[ch],
                self.slider_last, self.classif_regions[ch],
                self.portion_regions[ch], self.classified_pos)

            self.all_data_plots[ch].plot(ch_data, pen='w')
            self.full_graph.connect_slider(ch, self.update_slider_graph)
            # self.add_sliders(ch, N_DATA)                                       # improve the code
            self.add_sliding_region(ch)
            # Create classification graph and plot
            self.classify_ch_data(ch, ch_data)
            self.classif_plots[ch].plot(self.classified_data[ch], pen='b')

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

    def add_sliding_region(self, no):
        """
        Add Sliding region on the graph that will be add where experiment
        events occured during the training
        """

        self.full_graph.add_sliding_region(no)                                 # improve

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
        region.setRegion([no - 60, no + 110])
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
            [self.classified_pos, self.classified_pos + self.emg_signal_len])
        self.portion_regions[ch].setBrush(pale_red)
        # Classification graph (line down)
        self.classif_regions.append(pg.LinearRegionItem())
        self.classif_plots[ch].addItem(self.classif_regions[ch])
        self.classif_regions[ch].setRegion(
            [self.classified_pos, self.classified_pos])
        self.classif_regions[ch].setBrush(pale_red)
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
        self.portion_ch_layouts[ch].addWidget(self.portion_plots[ch], ch*2,3)
        # Classification plot
        self.portion_ch_layouts[ch].addWidget(self.classif_plots[ch], ch*2+1,3)
        self.portion_ch_layouts[ch].addWidget(self.avg_classif_plots[ch], ch*2, 0, 2, 3)
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




