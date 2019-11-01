# -- General Packages --
from PyQt5.QtWidgets import *
import numpy as np
import pyqtgraph as pg
# -- My Packages --
from V2.GUI.tabs.inner_dock import InnerDock


class ClassificationGraphDock(InnerDock):
    def __init__(self, ch):
        super().__init__(f'{ch+1}', toggle_btn=False, hide_title=True,
            auto_orientation=True, background_color=(0, 0, 0))


        self.N_DATA_TOT = 100
        self.left_bound = 10
        self.right_bound = 20
        self.plot_width = self.right_bound - self.left_bound

        self._plot, self.curve = self.init_plot(n_curves=3)
        self.region = self._init_region(self._plot)
        self._init_combobox()

    def _init_combobox(self):
        self._combobox = QComboBox()
        self._combobox.setStyleSheet(
            'QComboBox'
            # '{background-color: rgba(170, 170, 170, 200);'
            '{background-color: rgba(30, 80, 105, 120);'
            # '{background-color: rgba(20, 20, 70, 100);'
            'color:white;'
            'selection-background-color: darkblue;'
            'border: 2px solid rgba(220, 220, 220, 100);}'
            'QListView{color:red; background-color:black}')
        for val in ['1', '2', '3']:
            self._combobox.addItem(val)
        self.addWidget(self._combobox, 1, 0)

    def init_plot(
            self, pos=(0, 0), size=(1, 1), data=np.random.random(10000),
            n_curves=1):
        plot = pg.PlotWidget()
        color = ['g', 'r', 'b']
        for i in range(n_curves):
            curve = plot.plot(np.random.random(100))
            curve.setPen(color[i])
            plot.plotItem.setXRange(self.left_bound, self.right_bound)
        self.inner_layout.addWidget(plot, *pos, *size)
        return plot, curve

    def _init_region(
            self, plot=None, bounds=(12, 16), movable=True,
            brush_color=(0, 0, 250, 50)):
        """ Add a pyqtgraph region on a single event """
        region = pg.LinearRegionItem(movable=movable)
        # region.setMovable(False)
        region.setRegion(bounds)
        # region.start_pos = bounds[0]
        # region.last_pos = bounds[0]
        plot.addItem(region)
        region.setBrush(brush_color)
        return region

    def update(self, signal):
        self.curve.setData(signal)

