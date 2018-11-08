from PyQt5.QtWidgets import *
import pyqtgraph as pg
from PyQt5.QtCore import Qt


class FullGraph:
    def __init__(self):
        self.regions = []
        self.full_ch_layouts = []
        self.all_data_plots = []
        self.sliders = []
        self.full_graph_x_range = 8000

        self.full_graph_group, self.full_graph_layout = self.create_full_graph()

    def create_full_graph(self):
        self.full_graph_layout = QGridLayout()
        full_graph_group = QGroupBox('Full graph')
        full_graph_group.setLayout(self.full_graph_layout)
        return full_graph_group, self.full_graph_layout

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
        self.full_ch_layouts[ch].addWidget(self.all_data_plots[ch], ch*2+1, 0)
        # Add these group by channel to the right side of the separation
        self.full_graph_layout.addWidget(self.full_graph_ch_group)

    def add_sliders(self, ch, N_DATA):
        # # Slider to scoll through all data
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, N_DATA)
        self.full_ch_layouts[ch].addWidget(self.slider, ch*2+2, 0)

    def connect_slider(self, ch, update_slider_graph):
        self.sliders.append(update_slider_graph)
        self.slider.valueChanged.connect(self.sliders[ch].update_graph_range)

    def add_sliding_region(self, no):
        """
        Add Sliding region on the graph that will be add where experiment
        events occured during the training
        """
        # (ignoreBounds) Tells the ViewBox to exclude this item when doing
        # auto-range calculations.
        self.all_data_plots[no].addItem(self.regions[no], ignoreBounds=True)
        # Activate ability for the graph to scale the y axis
        self.all_data_plots[no].setAutoVisible(y=True)

