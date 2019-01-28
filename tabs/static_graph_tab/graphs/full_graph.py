# -- General packages --
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
# -- My packages --
from ... static_graph_tab.graphs.graph import Graph


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