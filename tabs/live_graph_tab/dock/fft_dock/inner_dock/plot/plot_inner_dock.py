# --General Packages--
import pyqtgraph as pg
from collections import deque
from functools import partial
import numpy as np
# --My Packages--
from app.colors import *
from tabs.live_graph_tab.dock.inner_dock import InnerDock
from .filter_region import FilterRegion


class PlotInnerDock(InnerDock):
    def __init__(self, gv, layout):
        super().__init__(layout, 'plot')

        self.gv = gv

        self.freq_curves = []

        self.plot = self._init_plot()

    def _init_plot(self):
        plot = self._set_plot_settings()
        self._add_plot(plot)
        self._add_curves_to_plot(plot)
        self.add_filter_to_plot(plot)
        return plot

    def _set_plot_settings(self):
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        plot.plotItem.setLabel(axis='bottom', text='Frequency', units='Hz')     # TODO: ALEXM : verifier l'uniter
        plot.plotItem.setLabel(axis='left', text='Amplitude', units='None')
        plot.setXRange(0, 130)
        plot.setYRange(0, 1000000)
        return plot

    def _add_plot(self, plot):
        self.layout.addWidget(plot, 2, 0, 5, 5)

    def _add_curves_to_plot(self, plot):
        for ch in range(self.gv.N_CH):
            self.freq_curves.append(
                plot.plot(
                    deque(np.ones(self.gv.DEQUE_LEN),
                          maxlen=self.gv.DEQUE_LEN)))
            self.freq_curves[ch].setPen(pen_colors[ch])
        # Keep track of the curve value in the dispatcher
        self.gv.freq_curves = self.freq_curves
        return plot

    def add_filter_to_plot(self, plot):
        # Pass filter
        pass_filter = FilterRegion(
                self.gv, type='pass', color=blue,
                min_boundary=self.gv.min_pass_filter,
                max_boundary=self.gv.max_pass_filter)
        plot.addItem(pass_filter.region)
        # Cut filter
        cut_filter = FilterRegion(
                self.gv, type='cut', color=red,
                min_boundary=self.gv.min_cut_filter,
                max_boundary=self.gv.max_cut_filter)
        plot.addItem(cut_filter.region)

