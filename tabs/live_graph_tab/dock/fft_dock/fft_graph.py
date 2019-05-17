# -*- coding: utf-8 -*-
# -- General packages --

import pyqtgraph as pg
from pyqtgraph import parametertree as ptree
from pyqtgraph.widgets.DataFilterWidget import DataFilterParameter
from pyqtgraph.graphicsItems.TextItem import TextItem
from pyqtgraph import getConfigOption

from collections import deque
import numpy as np
from functools import partial
from pyqtgraph.dockarea import *
# -- My packages --
from app.colors import *
from ... dock.dock import Dock
from tabs.live_graph_tab.dock.inner_dock import InnerDock
import pyqtgraph.metaarray as metaarray
from . settings_inner_dock import SettingsInnerDock


class FftGraphDock:
    def __init__(self, gv, layout):
        self.gv = gv
        self.layout = layout

        self.freq_curves = []

        self.dock_area = DockArea()
        layout.addWidget(self.dock_area, 1, 0, 1, 8)

        # Plot
        self.plot = self._init_plot()
        self.add_regions_filter_to_plot()
        self.connect_classif_region()

        # Settings
        self.settings_inner_dock = SettingsInnerDock(self.gv, self)
        self.dock_area.addDock(self.settings_inner_dock.dock, 'top')

        # Filter settings
        self.filter_inner_dock = self.init_filter_inner_dock()

    def _init_plot(self):
        plot = self._set_plot_settings()
        dock = self._init_dock()
        self._add_plot_to_dock(plot, dock)
        self._add_curves_to_plot(plot)
        return plot

    def _set_plot_settings(self):
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        plot.plotItem.setLabel(axis='bottom', text='Frequency', units='Hz')    # TODO: ALEXM : verifier l'uniter
        plot.plotItem.setLabel(axis='left', text='Amplitude', units='None')
        plot.setXRange(0, 130)
        plot.setYRange(0, 1000000)
        return plot

    def _init_dock(self):
        plot_d = InnerDock(self.layout, 'plot')
        self.dock_area.addDock(plot_d.dock)
        return plot_d

    def _add_plot_to_dock(self, plot, dock):
        dock.layout.addWidget(plot, 2, 0, 5, 5)

    def _add_curves_to_plot(self, plot):
        for ch in range(self.gv.N_CH):
            self.freq_curves.append(
                plot.plot(deque(np.ones(self.gv.DEQUE_LEN),
                                maxlen=self.gv.DEQUE_LEN)))
            self.freq_curves[ch].setPen(pen_colors[ch])
        # Keep track of the curve value in the dispatcher
        self.gv.freq_curves = self.freq_curves
        return plot

    def add_regions_filter_to_plot(self):
        """Add a region to the plot that will be use as the bondaries for
        the filter (blue for pass and red for cut)"""
        # Band pass filter
        self.pass_f_region = pg.LinearRegionItem(
                values=[self.gv.min_pass_filter, self.gv.max_pass_filter],
                brush=blue)
        self.plot.addItem(self.pass_f_region)
        # Band cut filter
        self.cut_f_region = pg.LinearRegionItem(
                values=[self.gv.min_cut_filter, self.gv.max_cut_filter],
                brush=red)
        self.plot.addItem(self.cut_f_region)

    def connect_classif_region(self):
        self.pass_f_region.sigRegionChanged.connect(
                partial(self.update_pass_filter_region))
        self.cut_f_region.sigRegionChanged.connect(
                partial(self.update_cut_filter_region))

    def update_pass_filter_region(self):
        self.gv.min_pass_filter, self.gv.max_pass_filter = \
                self.pass_f_region.getRegion()

    def update_cut_filter_region(self):
        self.gv.min_cut_filter, self.gv.max_cut_filter = \
                self.cut_f_region.getRegion()

    def init_filter_inner_dock(self):
        inner_dock = InnerDock(
            self.layout, 'Filter', toggle_button=True,
            size=(1, 1), b_pos=(0, 1), b_checked=False)
        self.dock_area.addDock(inner_dock.dock, 'right')
        inner_dock.dock.hide()
        return inner_dock

