# -- General Packages --
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np
# -- My Packages --
from V2.GUI.tabs.inner_dock import InnerDock
from functools import partial


class FullGraphDock(InnerDock):
    def __init__(self, ch):
        super().__init__(f'{ch+1}', toggle_btn=False, hide_title=True,
            auto_orientation=True, background_color=(0, 0, 0))

        self.N_DATA_TOT = 100
        self.left_bound = 10
        self.right_bound = 20
        self.plot_width = self.right_bound - self.left_bound

        self._ch = ch
        # data = self._loat_data()
        # self._plot = self._init_plot(data=data)
        #
        self.plot, self.curve = self.init_plot()

        self.slider = self._init_slider()

        region = pg.LinearRegionItem(values=(12, 16), brush=(0, 0, 250, 50))
        self.plot.addItem(region)

    def init_plot(
            self, pos=(0, 0), size=(1, 1), data=np.random.random(100)):
        plot = pg.PlotWidget()
        curve = plot.plot(data)
        curve.setPen('b')
        self.inner_layout.addWidget(plot, *pos, *size)
        return plot, curve

    def _init_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, self.N_DATA_TOT)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(self.N_DATA_TOT // 10)
        self.addWidget(slider)
        return slider

    def update(self, signal):
        self.curve.setData(signal)

    def connect_slider(self):
        self.slider.valueChanged[int].connect(
            partial(self.print_pos))

    def print_pos(self, value):
        print(value)

