from PyQt5.QtWidgets import *
import pyqtgraph as pg
from PyQt5.QtCore import Qt


class FullGraph:
    def __init__(self):
        self.regions = []
        self.layouts = []
        self.plots = []
        self.sliders = []
        self.x_range = 8000

        self.group_box, self.layout = self.create_group_and_layout()

    def create_group_and_layout(self):
        layout = QGridLayout()
        group_box = QGroupBox('Full graph')
        group_box.setLayout(layout)
        return group_box, layout

    def add_full_static_graph(self, ch):
        # Full graph
        self.layouts.append(QGridLayout())
        self.graph_group = QGroupBox(f'ch {ch+1}')
        self.graph_group.setLayout(self.layouts[ch])
        # Region of selection in the 'all_data_plot'
        self.regions.append(pg.LinearRegionItem())
        # Instanciate the plot containing all the data
        self.plots.append(pg.PlotWidget())
        self.plots[ch].setXRange(0, self.x_range)
        # All the values open from the saved file
        self.layouts[ch].addWidget(self.plots[ch], ch*2+1, 0)
        # Add these group by channel to the right side of the separation
        self.layout.addWidget(self.graph_group)

    def add_sliders(self, ch, N_DATA):
        # # Slider to scoll through all data
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, N_DATA)
        self.layouts[ch].addWidget(self.slider, ch*2+2, 0)

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

