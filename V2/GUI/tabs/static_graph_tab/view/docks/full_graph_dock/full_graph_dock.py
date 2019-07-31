# -- General Packages --
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
# -- My Packages --
from V2.GUI.tabs.static_graph_tab.view.static_graph_dock import StaticGraphDock
from functools import partial


class FullGraphDock(StaticGraphDock):
    def __init__(self, ch):
        super().__init__(ch)

        self._ch = ch
        # data = self._loat_data()
        # self._plot = self._init_plot(data=data)
        #
        self.plot, self.curve = self.init_plot()

        self.slider = self._init_slider()
        self.region = self._init_region(self.plot)

    def connect_slider(self):
        self.slider.valueChanged[int].connect(
            partial(self.print_shit))

    def print_shit(self, value):
        print('shit', value)

    def _init_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, self.N_DATA_TOT)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(self.N_DATA_TOT // 10)
        self.addWidget(slider)
        return slider


