from collections import deque
import numpy as np
from numpy.fft import fft, fftfreq
import pyqtgraph as pg
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot

import pyqtgraph as pg
from pyqtgraph.dockarea import *


class FftGraph:
    """
    """
    def __init__(self, main_window, fft_layout, timer_fft, gv, pen_color):
        self.main_window = main_window
        self.fft_layout = fft_layout
        self.timer_fft = timer_fft
        self.gv = gv
        self.pen_color = pen_color

        self.N_DATA = self.gv.DEQUE_LEN
        self.curve_freq = []
        
        self.init_fft_plot()

    def init_fft_plot(self):
        """
        """
        # Create the plot widget and its characteristics
        self.fft_plot = pg.PlotWidget(background=(3, 3, 3))
        self.fft_plot.plotItem.showGrid(x=False, y=True, alpha=0.3)
        self.fft_plot.plotItem.setLabel(axis='bottom', text='Frequency',
                                   units='Hz')                                 # Todo : ALEXM : verifier l'uniter
        self.fft_plot.plotItem.setLabel(axis='left', text='Amplitude',
                                   units='None')
        # Add to tab layout
        self.fft_layout.addWidget(self.fft_plot, 1, 0, 1, 1)
        for ch in range(self.gv.N_CH):
            self.curve_freq.append(
                self.fft_plot.plot(deque(np.zeros(self.N_DATA), maxlen=self.N_DATA)))
        # Associate the plot to an FftGraph object
        self.timer_fft.timeout.connect(self.update_fft_plotting)
        # Create the on button
        self.fft_on_off_button()

    def update_fft_plotting(self):
        remove_first_data = 2
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
            self.curve_freq[ch].setPen(self.pen_color[ch])

    def fft_on_off_button(self):
        b = QPushButton('Show FFT', self.main_window)
        b.setStyleSheet("background-color: rgba(0, 0, 80, 0.4)")
        self.fft_layout.addWidget(b, 0, 0, 1, 1)
        b.setCheckable(True)
        b.toggled.connect(partial(self.start_fft))

    @QtCore.pyqtSlot(bool)
    def start_fft(self, checked):
        if checked:
            self.timer_fft.start(250)
        else:
            self.timer_fft.stop()
