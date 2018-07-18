# -*- coding: utf-8 -*-

# PLOTING the EEG data
# Graph the data
from PyQt5 import QtGui, QtCore
from pyqtgraph.Qt import QtGui
import numpy as np
import pyqtgraph as pg
from collections import deque
import threading
from numpy.fft import fft, fftfreq
# My packages
from frequency_counter import FrequencyCounter
import sched, time


class EEG_graph(object):
    def __init__(self, eeg_plot, one_ch_deque, n_data_created):
        self.one_ch_deque = one_ch_deque
        self.n_data_created = n_data_created[0]

        self.N_DATA = len(one_ch_deque)
        self.curve_eeg = eeg_plot.plot(deque(np.zeros(self.N_DATA),
                                             maxlen=self.N_DATA))

    def update_eeg_plotting(self):
        # if self.n_data_created % 10 == 0:
        self.curve_eeg.setData(self.one_ch_deque)


class FFT_graph(object):
    def __init__(self, freq_plot, data_queue, n_data_created):
        self.data_queue = data_queue[0]
        self.n_data_created = n_data_created

        self.N_DATA = len(self.data_queue)
        self.curve_freq = freq_plot.plot(deque(np.ones(self.N_DATA),
                                               maxlen=self.N_DATA))

    def update_fft_plotting(self):
        # Calculate FFT
        if self.n_data_created[0] % 10 == 0:
            ch_fft = fft(self.data_queue)
            self.curve_freq.setData(abs(ch_fft[:len(ch_fft) // 2]))                                                      # TODO: ALEXM prendre abs ou real? avec real il y a des valeurs negatives est-ce que c'est normal?


class MultiChannelsPyQtGraph(object):
    def __init__(self, data_queue, n_data_created):
        """

        """
        self.data_queue = data_queue
        # self.win = pg.GraphicsWindow()

        self.n_data_created = n_data_created
        self.N_CH = len(self.data_queue)
        self.eeg_plots = []

        self.init_pyqt()
        self.init_eeg_plot()
        self.init_fft_plot()
        # FFT_graph.__init__(self, self.data_queue, self.n_data_created,)
        # EEG_graph.__init__(self, self.data_queue)

    def init_pyqt(self):
        # PyQt5 elements
        app = pg.mkQApp()
        self.b_loc = QtGui.QPushButton('plot local')
        self.b_cris = QtGui.QPushButton('plot a une autre place crisss')
        # Build the layout
        self.layout = pg.LayoutWidget()
        self.layout.addWidget(self.b_loc)
        self.layout.addWidget(self.b_cris)
        self.layout.resize(1000, 800)
        self.layout.show()
        self.timer = QtCore.QTimer()

    def init_eeg_plot(self):
        for ch in range(self.N_CH):
            plot = pg.PlotWidget()
            self.layout.addWidget(plot, row=ch+1, col=0, rowspan=1)
            self.eeg_plots.append(EEG_graph(plot, self.data_queue[ch], self.n_data_created))
            self.timer.timeout.connect(self.eeg_plots[ch].update_eeg_plotting)

    def init_fft_plot(self):
        plot = pg.PlotWidget()
        self.layout.addWidget(plot, row=1, col=1, rowspan=8)
        self.fft_plot = FFT_graph(plot, self.data_queue, self.n_data_created)
        self.timer.timeout.connect(self.fft_plot.update_fft_plotting)

    def exec_plot(self):
        self.timer.start(0)
        QtGui.QApplication.instance().exec_()






