# -*- coding: utf-8 -*-

# PLOTING the EEG data
# Graph the data
from PyQt5.QtWidgets import (QLineEdit, QSlider, QPushButton, QVBoxLayout,
                             QApplication, QWidget, QLabel, QCheckBox,
                             QRadioButton,QTextEdit, QHBoxLayout, QFileDialog,
                             QAction, qApp, QMainWindow, QMenuBar, QSlider)
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
# from pyqtgraph.Qt import QtGui
import numpy as np
import pyqtgraph as pg
from collections import deque
import threading
from numpy.fft import fft, fftfreq
# My packages
from frequency_counter import FrequencyCounter
import sched, time
import sys


class EEG_graph(object):
    """

    """
    def __init__(self, eeg_plot, one_ch_deque, n_data_created, pen_color):
        self.one_ch_deque = one_ch_deque
        self.n_data_created = n_data_created[0]

        self.N_DATA = len(one_ch_deque)
        self.curve_eeg = eeg_plot.plot(deque(np.zeros(self.N_DATA),
                                             maxlen=self.N_DATA))
        self.curve_eeg.setPen(pen_color)

    def update_eeg_plotting(self):
        # if self.n_data_created % 10 == 0:
        self.curve_eeg.setData(self.one_ch_deque)


class FFT_graph(object):
    """

    """
    def __init__(self, freq_plot, data_queue, n_data_created, pen_color):
        self.data_queue = data_queue
        self.n_data_created = n_data_created
        self.freq_plot = freq_plot
        self.pen_color = pen_color

        self.N_DATA = len(self.data_queue[0])
        self.N_CH = len(self.data_queue)

        self.curve_freq = []
        for ch in range(self.N_CH):
            self.curve_freq.append(freq_plot.plot(deque(np.ones(self.N_DATA),
                                                   maxlen=self.N_DATA)), )

    def update_fft_plotting(self):
        # Calculate FFT
        if self.n_data_created[0] % 100 == 0:
            for ch in range(self.N_CH):
                ch_fft = fft(self.data_queue[ch])
                self.curve_freq[ch].setData(abs(ch_fft[:len(ch_fft) // 2]))      # TODO: ALEXM prendre abs ou real? avec real il y a des valeurs negatives est-ce que c'est normal?
                self.curve_freq[ch].setPen(self.pen_color[ch])





#IIIIIIIIIIIIIIIIIICCCCCCCCCCCCCCCCCCCCIIIIIIIIIIIIIIIIIIIIII








class MultiChannelsPyQtGraph(QMainWindow):
    def __init__(self, data_queue, n_data_created):
        """

        """
        super(MultiChannelsPyQtGraph, self).__init__()
        self.data_queue = data_queue
        self.pen_color = ['r', 'y', 'g', 'c', 'b', 'm', (100, 100, 100), 'w']
        self.button_color = ['red', 'yellow', 'green', 'cyan',
                             'blue', 'magenta', 'grey', 'white']
        self.BUTTON_PER_CH = 2

        self.n_data_created = n_data_created
        self.N_CH = len(self.data_queue)
        self.eeg_plots = []

        # Init all the main part of the window
        self.init_pyqt()
        self.init_eeg_plot()
        self.init_fft_plot()

    def init_pyqt(self):
        """

        """
        self.setWindowTitle('PolyCOOL cest trop cool')
        self.timer = QtCore.QTimer()
        # PyQt5 elements
        self.b_EEG = QtGui.QPushButton('EEG plots')
        self.b_FFT = QtGui.QPushButton('FFT plot')
        # Create the layout
        self.layout = pg.LayoutWidget()
        self.layout.addWidget(self.b_EEG, row=0, col=1)
        self.layout.addWidget(self.b_FFT, row=0, col=3)
        # Assign number to each channel
        self.assign_n_to_ch()
        # Assign button for action on every channel
        self.assign_action_to_ch()
        # Create the menu
        self.create_menu_bar()

        self.statusBar().showMessage('Message in statusbar.')
        self.setCentralWidget(self.layout)
        self.setGeometry(100, 100, 1200, 900)
        self.show()

    def assign_n_to_ch(self):
        for ch in range(self.N_CH):
            b_on_off_ch = QtGui.QPushButton(str(ch))
            style = ('QPushButton {background-color'
                                + ': {color}; '.format(color=self.button_color[ch])
                                + 'min-width: 14px}')
            b_on_off_ch.setStyleSheet(style)
            self.layout.addWidget(item=b_on_off_ch, row=ch*3+2, col=0, rowspan=1)

    def assign_action_to_ch(self):
        for ch in range(self.N_CH):
            for b_n in range(self.BUTTON_PER_CH):
                b_action_ch = QtGui.QPushButton('act ' + str(ch*3 + b_n))
                b_action_ch.clicked.connect(self.print_allo)
                self.layout.addWidget(item=b_action_ch,
                                      row=ch*3 + b_n + 1, col=2, rowspan=1)

    def print_allo(self):
        print('allo les dudddes ... ')

    def create_menu_bar(self):
        main_menu = self.menuBar()
        menu_item = ['&File', '&Edit', '&View','&Navigate',
                     '&Code', '&Refactor', 'R&un', '&Tools']
        for item in menu_item:
            main_menu.addMenu(item)

    def init_eeg_plot(self):
        """

        """
        for ch in range(self.N_CH):
            plot = pg.PlotWidget(background=(3, 3, 3))
            plot.plotItem.showGrid(x=True, y=True, alpha=0.1)
            # Add the label only for the last channel as they all have the same
            if ch == 7:
                plot.plotItem.setLabel(axis='bottom', text='Time', units='s')  # Todo : ALEXM : verifier l'uniter
                plot.plotItem.setLabel(axis='left', text='Amplitude', units='v')
            self.layout.addWidget(plot, row=ch*3+1, col=1, rowspan=3)

            self.eeg_plots.append(EEG_graph(plot, self.data_queue[ch],
                                            self.n_data_created,
                                            self.pen_color[ch]))
            self.timer.timeout.connect(self.eeg_plots[ch].update_eeg_plotting)

    def init_fft_plot(self):
        """

        """
        plot = pg.PlotWidget(background=(3, 3, 3))
        plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        plot.plotItem.setLabel(axis='bottom', text='Frequency', units='Hz')   # Todo : ALEXM : verifier l'uniter
        plot.plotItem.setLabel(axis='left', text='Amplitude', units='None')
        self.layout.addWidget(plot, row=1, col=3, rowspan=12)
        self.fft_plot = FFT_graph(plot, self.data_queue, self.n_data_created,
                                  self.pen_color)
        self.timer.timeout.connect(self.fft_plot.update_fft_plotting)

    def start_timer(self):
        self.timer.start(0)
