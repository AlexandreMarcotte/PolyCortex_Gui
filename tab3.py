# Graph the data
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot

import pyqtgraph as pg

from functools import partial

# My packages
from generated_signal import read_data_from_file


class Tab3(object):
    def __init__(self, main_window, tab3, data_queue):
        self.main_window = main_window
        self.tab3 = tab3
        self.N_CH = len(data_queue)
        # Stationnary graph
        self.slider_last = 0
        self.static_graph_file_name = 'heart_beat.csv'

    def create_tab3(self):
        self.tab3.layout = QGridLayout(self.main_window)
        # Place things on a layout
        self.open_data_from_file()
        # Set the layout
        self.tab3.setLayout(self.tab3.layout)

    def open_data_from_file(self):
        # Create button to open date file
        chose_file = QtGui.QPushButton('Chose file containing data')
        chose_file.setStyleSheet("background-color: rgba(0, 0, 150, 0.5)")
        chose_file.clicked.connect(partial(self.open_static_data_file))
        row=0; col=3; rowspan=1; colspan=1
        self.tab3.layout.addWidget(chose_file, row, col, rowspan, colspan)
        # Create text box to show or enter path to data file
        self.data_path = QtGui.QLineEdit(self.static_graph_file_name)
        row=0; col=1; rowspan=1; colspan=2
        self.tab3.layout.addWidget(self.data_path, row, col, rowspan, colspan)
        # Read the data from the file
        self.open_file_b = QtGui.QPushButton('Open File')
        self.open_file_b.clicked.connect(partial(self.create_stationnary_plot))
        row=0; col=4; rowspan=1; colspan=1
        self.tab3.layout.addWidget(self.open_file_b, row, col, rowspan, colspan)

    @pyqtSlot()
    def open_static_data_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self.main_window,
                                                  "QFileDialog.getOpenFileName()",
                                                  "", "All Files (*);;Python Files (*.py)",
                                                  options=options)
        if file_name:
            self.data_path.setText(file_name)
            self.static_graph_file_name = file_name

    @pyqtSlot()
    def create_stationnary_plot(self):
        # Read data from file
        self.data = read_data_from_file(self.static_graph_file_name,
                                        n_ch=self.N_CH)
        N_DATA = len(self.data[0])

        self.static_graph_update = []
        self.sliders = []

        for graph_num, graph_data in enumerate(self.data):
            # Region of selection in the 'all_data_plot'
            self.region = pg.LinearRegionItem()
            # Instanciate the plot containing the crosshair
            self.crosshair_plot = pg.PlotWidget()
            # Instanciate the plot containing all the data
            self.all_data_plot = pg.PlotWidget()
            self.all_data_plot.setXRange(0, 2000)

            # Portion of the graph
            row=graph_num*2+1; col=1; rowspan=1; colspan=2
            self.tab3.layout.addWidget(self.crosshair_plot, row,
                                       col, rowspan, colspan)
            # All the values open from the saved file
            row=graph_num*2+1; col=3; rowspan=1; colspan=2
            self.tab3.layout.addWidget(self.all_data_plot, row,
                                       col, rowspan, colspan)
            # # Slider to scoll through all data
            self.slider = QSlider(Qt.Horizontal)
            self.slider.setMinimum(0)
            self.slider.setMaximum(N_DATA)
            row=graph_num*2+2; col=3; rowspan=1; colspan=2
            self.tab3.layout.addWidget(self.slider, row, col, rowspan, colspan)
            self.update_slider_graph = UpdateSliderGraph(self.slider,
                                                         self.all_data_plot,
                                                         self.region,
                                                         self.slider_last)
            self.sliders.append(self.update_slider_graph)
            self.slider.valueChanged.connect(
                self.sliders[graph_num].update_graph_range)

            # Tell the ViewBox to exclude this item when doing auto-range calculations.
            self.all_data_plot.addItem(self.region, ignoreBounds=True)
            self.crosshair_plot.setAutoVisible(y=True)

            self.crosshair_plot.plot(graph_data, pen="g")
            self.all_data_plot.plot(graph_data, pen="w")

            # Create 8 update function object, one for every plot
            self.static_graph_update.append(
                StaticGraphUpdate(self.region, self.crosshair_plot))

            # Connect all the update functions
            self.region.sigRegionChanged.connect(
                self.static_graph_update[graph_num].update_portion_plot_range)

            self.crosshair_plot.sigRangeChanged.connect(
                self.static_graph_update[graph_num].update_region)

            self.region.setRegion([0, 200])
            # Create the number button
            self.assign_n_to_ch()

    def assign_n_to_ch(self):
        for ch in range(self.N_CH):
            # +1 so the number str start at 1
            b_on_off_ch = QtGui.QPushButton(str(ch + 1))
            style = ('QPushButton { min-width: 14px}')
            b_on_off_ch.setStyleSheet(style)
            # Set position and size of the button values
            row=ch*2+1; col=0; rowspan=1
            self.tab3.layout.addWidget(b_on_off_ch, row, col, rowspan, 1)


class StaticGraphUpdate(object):
    def __init__(self, region, crosshair_plot):
        self.region = region
        self.crosshair_plot = crosshair_plot

    def update_region(self, window, viewRange):
        """ Update the range of the region"""
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def update_portion_plot_range(self):
        """ Update the cross_hair_plot range based on the region position """
        minX, maxX = self.region.getRegion()
        self.crosshair_plot.setXRange(minX, maxX, padding=0)


class UpdateSliderGraph(object):
    def __init__(self, slider, all_data_plot, region, slider_last):
        self.slider = slider
        self.all_data_plot = all_data_plot
        self.region = region
        self.slider_last = slider_last

    def update_graph_range(self):
        v = self.slider.value()
        # Keep track of the movement of the slider between two updates
        delta_slider = v - self.slider_last
        self.slider_last = v
        # Update the graph range based on the slider position
        self.all_data_plot.setXRange(v, v + 2000)
        r_right = self.region.boundingRect().right()
        r_left = self.region.boundingRect().left()
        # Update the region position based on the delta position of the slider
        self.region.setRegion([r_right + delta_slider, r_left + delta_slider])
