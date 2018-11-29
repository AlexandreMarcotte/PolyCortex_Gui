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
from pyqtgraph import functions as fn

from collections import deque
import numpy as np
import re
# -- My packages --
from app.colors import *
from app.activation_b import btn
from data_processing_pipeline.calcul_fft import FreqCalculator


class FftGraph:
    """
    """
    def __init__(self, gv, layout):
        self.gv = gv
        self.layout = layout

        plot_gr, self.plot_layout = self.create_gr()
        filter_gr, self.filter_layout = self.create_gr()
        splitter = self.create_splitter(plot_gr, filter_gr)
        self.layout.addWidget(splitter)

        self.timer = QtCore.QTimer()
        self.N_DATA = self.gv.DEQUE_LEN
        self.curve_freq = []
        
        self.plot = self.init_plot()
        self.add_regions_to_plot()
        self.add_param_tree()
        self.on_off_button()
        self.create_all_combobox()

    def create_gr(self):
        gr = QGroupBox()
        l = QGridLayout()
        gr.setLayout(l)
        return gr, l

    def create_splitter(self, first_gr, second_gr):
        s = QSplitter(Qt.Horizontal)
        s.addWidget(first_gr)
        s.addWidget(second_gr)
        return s

    def init_plot(self):
        """Create the plot widget and its characteristics"""
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        plot.plotItem.setLabel(axis='bottom', text='Frequency', units='Hz')    # TODO: ALEXM : verifier l'uniter
        plot.plotItem.setLabel(axis='left', text='Amplitude', units='None')
        # self.plot.setYRange(0, np.log(1500000))
        # Add to tab layout
        self.plot_layout.addWidget(plot, 2, 0, 1, 5)
        for ch in range(self.gv.N_CH):
            self.curve_freq.append(
                plot.plot(deque(np.ones(self.N_DATA), maxlen=self.N_DATA)))
        # Associate the plot to an FftGraph object
        self.timer.timeout.connect(self.update_plotting)
        return plot

    def add_param_tree(self):
        self.ptree = ptree.ParameterTree(showHeader=False)
        self.filter = DataFilterParameter()
        params = ptree.Parameter.create(name='params', type='group', children=[self.filter])
        self.ptree.setParameters(params, showTop=False)

        self.filter_layout.addWidget(self.ptree)

        # bg = fn.mkColor(getConfigOption('background'))
        # bg.setAlpha(150)
        self.filterText = TextItem(border=getConfigOption('foreground'))
        self.filterText.setPos(60,20)
        self.filterText.setParentItem(self.plot.plotItem)
        self.filter.sigFilterChanged.connect(self.filterChanged)
        self.filter.setFields([
            ('butterFilter', {'units': 'Hz'}),
        ])

    def filterChanged(self):
        print('cool')

    def add_regions_to_plot(self):
        """Add a region to the plot that will be use as the bondaries for
        the filter (blue for pass and red for cut"""
        self.plot.addItem(pg.LinearRegionItem([0, 100]), ignoreBounds=True)

    def update_plotting(self):
        self.all_frequency()

    def all_frequency(self):
        for ch in range(self.gv.N_CH):
            freq_calculator = FreqCalculator(
                remove_first_data=0, data_q=self.gv.data_queue[ch],
                t_q=self.gv.t_queue)
            freq_range = freq_calculator.get_freq_range()
            # Keep all frequency possibles                                     # TODO: ALEXM: Change frequency in function of time
            self.curve_freq[ch].setData(freq_range, freq_calculator.fft())                       # TODO: ALEXM prendre abs ou real? avec real il y a des valeurs negatives est-ce que c'est normal?
            self.curve_freq[ch].setPen(pen_colors[ch])

    def on_off_button(self):
        btn('Start FFT', self.plot_layout, (0, 0), func_conn=self.start,
            color=blue_b, toggle=True, txt_color=white)

    def create_all_combobox(self):
        self.create_param_combobox(
            'Max Freq', (0, 1),
            ['Auto', '60 Hz', '80 Hz', '100 Hz', '120 Hz'],
            self.scale_x_axis)
        self.create_param_combobox(
            'Max Uv', (0, 2),
            ['Auto','1000 uv', '10000 uv', '100000 uv', '1000000 uv',
             '10000000 uv'],
            self.scale_y_axis)
        self.create_param_combobox(
            'Log', (0, 3), ['False', 'True'], self.log_axis)
        self.create_param_combobox(
            'Ch ON', (0, 4),
            ['ch 1', 'ch 2', 'ch 3', 'ch 4', 'ch 5', 'ch 6', 'ch 7', 'ch 8'],
            self.ch_on_off, editable=False)

    def create_param_combobox(
            self, name, pos, param, conn_func, editable=True):
        label = QLabel(name)
        label.setFrameShape(QFrame.Panel)
        label.setFrameShadow(QFrame.Sunken)
        label.setLineWidth(1)
        label.setAlignment(Qt.AlignCenter)
        self.plot_layout.addWidget(label, *pos)
        vert_scale = QComboBox()
        for val in param:
            vert_scale.addItem(val)
        vert_scale.setEditable(editable)
        vert_scale.activated[str].connect(conn_func)
        self.plot_layout.addWidget(vert_scale, pos[0]+1, pos[1])

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
            self.timer.start(100)
        else:
            self.timer.stop()
