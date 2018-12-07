# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

import pyqtgraph as pg
from pyqtgraph import parametertree as ptree
from pyqtgraph.widgets.DataFilterWidget import DataFilterParameter
from pyqtgraph.graphicsItems.TextItem import TextItem
from pyqtgraph import getConfigOption

from collections import deque
import numpy as np
import re
from functools import partial
# -- My packages --
from app.colors import *
from app.activation_b import btn
from app.pyqt_frequently_used import (create_gr, create_txt_label,
                                      create_splitter, create_param_combobox,
                                      add_triplet_txt_box)
from ... dock.dock import Dock


class FftGraph:
    """
    """
    def __init__(self, gv, layout):
        self.gv = gv
        self.curve_freq = []

        self.init_layout(layout)
        self.init_on_off_button()
        self.timer = self.init_timer()

        self.plot = self.init_plot()
        self.add_regions_filter_to_plot()
        self.connect_classif_region()
        self.add_param_tree()
        self.create_all_combobox()

    def init_layout(self, layout):
        plot_gr, self.plot_layout = create_gr()
        filter_gr, self.filter_layout = create_gr()
        splitter = create_splitter(plot_gr, filter_gr)
        layout.addWidget(splitter, 1, 0)

    def init_timer(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update_plotting)
        return timer

    def init_plot(self):
        """Create the plot widget and its characteristics"""
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        plot.plotItem.setLabel(axis='bottom', text='Frequency', units='Hz')    # TODO: ALEXM : verifier l'uniter
        plot.plotItem.setLabel(axis='left', text='Amplitude', units='None')
        plot.setXRange(0, 100)
        plot.setYRange(0, 1000000)
        # Add to tab layout
        self.plot_layout.addWidget(plot, 2, 0, 1, 5)
        for ch in range(self.gv.N_CH):
            self.curve_freq.append(
                plot.plot(deque(np.ones(self.gv.DEQUE_LEN),
                                maxlen=self.gv.DEQUE_LEN)))
        # Associate the plot to an FftGraph object
        return plot

    def add_param_tree(self):
        self.ptree = ptree.ParameterTree(showHeader=False)
        self.filter = DataFilterParameter()
        params = ptree.Parameter.create(name='params', type='group', children=[self.filter])
        self.ptree.setParameters(params, showTop=False)

        self.filter_layout.addWidget(self.ptree)

        self.filterText = TextItem(border=getConfigOption('foreground'))
        self.filterText.setPos(60,20)
        self.filterText.setParentItem(self.plot.plotItem)
        self.filter.sigFilterChanged.connect(self.filterChanged)
        self.filter.setFields([
            ('butterFilter', {'units': 'Hz'}),
        ])

    def filterChanged(self):
        print('cool')

    def add_regions_filter_to_plot(self):
        """Add a region to the plot that will be use as the bondaries for
        the filter (blue for pass and red for cut"""
        # Band pass filter
        self.pass_f_region = pg.LinearRegionItem([self.gv.min_pass_filter,     # TODO: ALEXM: avoid redondancy in the creation of filters
                                                  self.gv.max_pass_filter])
        self.pass_f_region.setBrush(blue)
        self.plot.addItem(self.pass_f_region, ignoreBounds=True)
        # Band cut filter
        self.cut_f_region = pg.LinearRegionItem([self.gv.min_cut_filter,
                                                 self.gv.max_cut_filter])
        self.cut_f_region.setBrush(red)
        self.plot.addItem(self.cut_f_region, ignoreBounds=True)

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

    def update_plotting(self):
        self.all_frequency()

    def all_frequency(self):
        for ch in range(self.gv.N_CH):
            self.curve_freq[ch].setData(self.gv.freq_calculator.freq_range,
                                        self.gv.freq_calculator.fft[ch])       # TODO: ALEXM prendre abs ou real? avec real il y a des valeurs negatives est-ce que c'est normal?
            self.curve_freq[ch].setPen(pen_colors[ch])

    def init_on_off_button(self):
        btn('Start FFT', self.plot_layout, (0, 0), func_conn=self.start,
            color=blue_b, toggle=True, txt_color=white, min_width=100)

    def create_all_combobox(self):
        create_param_combobox(
            self.plot_layout, 'Max Freq', (0, 1),
            ['Auto', '60 Hz', '80 Hz', '100 Hz', '120 Hz'],
            self.scale_x_axis)
        create_param_combobox(
            self.plot_layout, 'Max Uv', (0, 2),
            ['Auto','1000 uv', '10000 uv', '100000 uv', '1000000 uv',
             '10000000 uv'], self.scale_y_axis)
        create_param_combobox(
            self.plot_layout, 'Log', (0, 3), ['False', 'True'], self.log_axis)
        create_param_combobox(
            self.plot_layout, 'Ch On', (0, 4),
            ['ch 1', 'ch 2', 'ch 3', 'ch 4', 'ch 5', 'ch 6', 'ch 7', 'ch 8'],
            self.ch_on_off, editable=False)

    def scale_x_axis(self, txt):                                             # TODO: ALEXM: remove the redundancy
        try:
            if txt == 'Auto':
                self.plot.enableAutoRange()
            else:
                r = int(re.search(r'\d+', txt).group())
                self.plot.setXRange(0, r)
        except AttributeError:
            print("Come on bro, this  value doesn't make sens")

    def log_axis(self, txt):
        if txt == 'True':
            self.plot.setLogMode(y=True)
        else:
            self.plot.setLogMode(y=False)

    def scale_y_axis(self, txt):
        try:
            if txt == 'Auto':
                self.plot.enableAutoRange()
            else:
                r = int(re.search(r'\d+', txt).group())
                self.plot.setYRange(0, r)
        except AttributeError:
            print("Come on bro, this  value doesn't make sens")

    def ch_on_off(self):
        pass

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        if checked:
            if not self.gv.freq_calculator.activated:
                self.gv.freq_calculator.timer.start(100)
                self.gv.freq_calculator.activated = True
            self.timer.start(100)
        else:
            self.timer.stop()
            self.gv.freq_calculator.timer.stop()
            self.gv.freq_calculator.activated = False
