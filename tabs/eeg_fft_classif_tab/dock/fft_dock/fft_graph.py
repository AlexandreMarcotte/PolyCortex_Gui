# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot

import pyqtgraph as pg
from pyqtgraph.dockarea import *

from collections import deque
import numpy as np
from numpy.fft import fft, fftfreq
from functools import partial

# -- My packages --
from app.colors import *
from app.activation_b import activation_b


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
        plot.plotItem.setLabel(axis='bottom', text='Frequency', units='Hz')                                 # Todo : ALEXM : verifier l'uniter
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
        # Associate the plot to an FftGraph object
        self.timer.timeout.connect(self.update_plotting)
        # Create the on button
        self.on_off_button()

    def update_plotting(self):
        remove_first_data = 2                                                  # TODO: ALEXM: Filter instead of removing them direcly like that
        # interval of time from the first to the last value that was add to the queue
        delta_t = (self.gv.t_queue[-1] - self.gv.t_queue[0])
        # Calculate FFT (Remove freq 0 because it gives a really high value on the graph
        freq_range = np.linspace(remove_first_data, self.N_DATA//2/delta_t,
                                 self.N_DATA//2 - remove_first_data)
        for ch in range(self.gv.N_CH):
            ch_fft = fft(self.gv.data_queue[ch])
            # Keep all frequency possibles                                                  # TODO: Change frequency in function of time
            self.curve_freq[ch].setData(freq_range,
                                        abs(ch_fft[remove_first_data:self.N_DATA//2]))         # TODO: ALEXM prendre abs ou real? avec real il y a des valeurs negatives est-ce que c'est normal?
            self.curve_freq[ch].setPen(pen_colors[ch])

    def on_off_button(self):
        activation_b(self.layout, 'Start FFT', self.start, (0, 0),
                     dark_blue, toggle=True)

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(100)
        else:
            self.timer.stop()
