# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot

import pyqtgraph as pg
from pyqtgraph.dockarea import *

from collections import deque
import numpy as np
from functools import partial

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

        self.timer = QtCore.QTimer()
        self.N_DATA = self.gv.DEQUE_LEN
        self.curve_freq = []
        
        self.init_plot()

    def init_plot(self):
        """
        """
        # Create the plot widget and its characteristics
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        plot.plotItem.setLabel(axis='bottom', text='Frequency', units='Hz')    # TODO: ALEXM : verifier l'uniter
        plot.plotItem.setLabel(axis='left', text='Amplitude', units='None')
        plot.setXRange(0, 180)
        plot.setYRange(0, 1500000)
        # self.plot.setLogMode(y=True)
        # self.plot.setYRange(0, np.log(1500000))
        # Add to tab layout
        self.layout.addWidget(plot, 1, 0)
        for ch in range(self.gv.N_CH):
            self.curve_freq.append(
                plot.plot(deque(np.ones(self.N_DATA), maxlen=self.N_DATA)))
        self.layout.addWidget(self.graph_freq_type_combo(), 2, 0)
        # Associate the plot to an FftGraph object
        self.timer.timeout.connect(self.update_plotting)
        # Create the on button
        self.on_off_button()

    def update_plotting(self):
        for ch in range(self.gv.N_CH):
            freq_calculator = FreqCalculator(
                remove_first_data=2, data_q=self.gv.data_queue[ch],
                t_q=self.gv.t_queue)
            freq_range = freq_calculator.get_freq_range()
            # Keep all frequency possibles                                     # TODO: ALEXM: Change frequency in function of time
            self.curve_freq[ch].setData(freq_range, freq_calculator.fft())                       # TODO: ALEXM prendre abs ou real? avec real il y a des valeurs negatives est-ce que c'est normal?
            self.curve_freq[ch].setPen(pen_colors[ch])

    def on_off_button(self):
        btn('Start FFT', self.layout, (0, 0), func_conn=self.start,
            color=blue_b, toggle=True)

    def graph_freq_type_combo(self):
        graph_type = QComboBox()
        graph_type.addItem('All frequency')
        graph_type.addItem('Band frequency')
        graph_type.addItem('2D time FFT')
        return graph_type

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(100)
        else:
            self.timer.stop()
