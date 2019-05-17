# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5 import QtCore

import pyqtgraph as pg
from pyqtgraph import parametertree as ptree
from pyqtgraph.widgets.DataFilterWidget import DataFilterParameter
from pyqtgraph.graphicsItems.TextItem import TextItem
from pyqtgraph import getConfigOption

from collections import deque
import numpy as np
import re
from functools import partial
from pyqtgraph.dockarea import *
from pyqtgraph.flowchart import Flowchart
# -- My packages --
from app.colors import *
from app.activation_b import btn
from app.pyqt_frequently_used import create_param_combobox
from ... dock.dock import Dock
from tabs.live_graph_tab.dock.inner_dock import InnerDock
import pyqtgraph.metaarray as metaarray


class FftGraph:
    """
    """
    def __init__(self, gv, layout):
        self.gv = gv
        self.curve_freq = []
        self.layout = layout

        self.dock_area = DockArea()
        layout.addWidget(self.dock_area, 1, 0, 1, 8)
        # Plot
        self.ch_to_show = list(range(self.gv.N_CH))
        self.plot_d = self.init_plot_dock()
        self.plot = self.init_plot()
        self.add_regions_filter_to_plot()
        self.connect_classif_region()
        # Settings
        self.create_settings_dock()
        # Filter settings
        self.filter_d = self.create_filter_settings_dock()

        self.timer = self.init_timer()

    def init_plot_dock(self):
        plot_d = InnerDock(self.layout, 'plot')
        self.dock_area.addDock(plot_d.dock)
        return plot_d

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
        plot.setXRange(0, 130)
        plot.setYRange(0, 1000000)
        # Add to tab layout
        self.plot_d.layout.addWidget(plot, 2, 0, 5, 5)
        for ch in range(self.gv.N_CH):
            self.curve_freq.append(
                plot.plot(deque(np.ones(self.gv.DEQUE_LEN),
                                maxlen=self.gv.DEQUE_LEN)))
            self.curve_freq[ch].setPen(pen_colors[ch])

        self.gv.curve_freq = self.curve_freq
        return plot

    def add_param_tree(self):
        self.ptree = ptree.ParameterTree(showHeader=False)
        self.filter = DataFilterParameter()
        params = ptree.Parameter.create(
                name='params', type='group', children=[self.filter])
        self.ptree.setParameters(params, showTop=False)

        self.filter_layout.addWidget(self.ptree)

        self.filterText = TextItem(border=getConfigOption('foreground'))
        self.filterText.setPos(60, 20)
        self.filterText.setParentItem(self.plot.plotItem)
        self.filter.sigFilterChanged.connect(self.filterChanged)
        self.filter.setFields([('butterFilter', {'units': 'Hz'})])

    def filterChanged(self):
        print('cool')

    def add_regions_filter_to_plot(self):
        """Add a region to the plot that will be use as the bondaries for
        the filter (blue for pass and red for cut)"""
        # Band pass filter
        self.pass_f_region = pg.LinearRegionItem(
                [self.gv.min_pass_filter, self.gv.max_pass_filter])            # TODO: ALEXM: avoid redondancy in the creation of filters
        self.pass_f_region.setBrush(blue)
        self.plot.addItem(self.pass_f_region, ignoreBounds=True)
        # Band cut filter
        self.cut_f_region = pg.LinearRegionItem(
                [self.gv.min_cut_filter, self.gv.max_cut_filter])
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
        # for ch in range(self.gv.N_CH):
        for ch in self.ch_to_show:
            f_range, fft = self.gv.freq_calculator.get_fft_to_plot(
                    np.array(self.gv.data_queue[ch])[
                    self.gv.filter_min_bound:self.gv.filter_max_bound])
            self.curve_freq[ch].setData(f_range, fft)
            # self.curve_freq[ch].setData(
            #         self.gv.freq_calculator.freq_range,
            #         self.gv.freq_calculator.fft[ch])                         # TODO: ALEXM prendre abs ou real? avec real il y a des valeurs negatives est-ce que c'est normal?

    def init_on_off_button(self, layout):
        btn('Start', layout, (0, 0), func_conn=self.start,
            color=dark_blue_tab, toggle=True, txt_color=white, min_width=100)

    def create_settings_dock(self):
        settings_d = InnerDock(
            self.layout, 'Settings', toggle_button=True, size=(1, 1))
        self.init_on_off_button(settings_d.layout)

        create_param_combobox(
                settings_d.layout, 'Max Freq', (0, 1),
                ['Auto', '60 Hz', '80 Hz', '100 Hz', '120 Hz'],
                partial(self.scale_axis, axis_name='x'))
        create_param_combobox(
                settings_d.layout, 'Max Uv', (0, 2),
                ['Auto','1000 uv', '10000 uv', '100000 uv', '1000000 uv',
                 '10000000 uv'], partial(self.scale_axis, axis_name='y'))
        create_param_combobox(
                settings_d.layout, 'Log', (0, 3), ['False', 'True'],
                self.log_axis)
        create_param_combobox(
                settings_d.layout, 'Filter', (0, 4), ['No filter',
                'Bandpass', 'Bandstop', 'Both'],
                self.show_filter)
        self.combo_to_filter = {
                'No filter': [], 'Bandpass': ['bandpass'],
                'Bandstop': ['bandstop'], 'Both': ['bandpass', 'bandstop']}
        create_param_combobox(
                settings_d.layout, 'Ch On', (0, 5),
                ['ch 1', 'ch 2', 'ch 3', 'ch 4',
                 'ch 5', 'ch 6', 'ch 7', 'ch 8', 'all'],
                self.ch_on_off, editable=False)

        self.dock_area.addDock(settings_d.dock, 'top')

    def create_filter_settings_dock(self):
        filter_d = InnerDock(
                self.layout, 'Filter', toggle_button=True,
                size=(1, 1), b_pos=(0, 1), b_checked=False)
        self.dock_area.addDock(filter_d.dock, 'right')
        filter_d.dock.hide()
        return filter_d

    def scale_axis(self, txt, axis_name):
        try:
            if txt == 'Auto':
                self.plot.enableAutoRange()
            else:
                r = int(re.search(r'\d+', txt).group())
                if axis_name == 'x':
                    self.plot.setXRange(0, r)
                elif axis_name == 'y':
                    self.plot.setYRange(0, r)
        except AttributeError:
            print("Come on bro, this  value doesn't make sens")

    def log_axis(self, txt):
        self.plot.setLogMode(y=eval(txt))

    def ch_on_off(self, ch):
        if ch == 'all':
            self.ch_to_show = list(range(self.gv.N_CH))
        else:
            self.ch_to_show = [int(ch[3:]) - 1]
        self.clear_curves()

    def clear_curves(self):
        for c in self.curve_freq:
            c.clear()

    def show_filter(self, txt):
        self.gv.filter_to_use = self.combo_to_filter[txt]

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
