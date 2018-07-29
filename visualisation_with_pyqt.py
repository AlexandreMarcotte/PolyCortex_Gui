# -*- coding: utf-8 -*-

# PLOTING the EEG data
# Graph the data
from PyQt5.QtWidgets import (QLineEdit, QSlider, QPushButton, QVBoxLayout,
                             QApplication, QWidget, QLabel, QCheckBox,
                             QRadioButton,QTextEdit, QHBoxLayout, QFileDialog,
                             QAction, qApp, QMainWindow, QMenuBar, QSlider,
                             QGridLayout, QTabWidget)
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


class App(QMainWindow):

    def __init__(self, data_queue, n_data_created):
        super().__init__()
        self.setWindowTitle('basic graph')
        # Add a menu bar
        self.create_menu_bar()
        # message at the bottom
        self.statusBar().showMessage('Message in statusbar.')

        self.simple_graph = MultiChannelsPyQtGraph(data_queue, n_data_created)
        self.setCentralWidget(self.simple_graph)
        self.simple_graph.start_timer()

        self.show()

    def create_menu_bar(self):
        main_menu = self.menuBar()
        menu_item = ['&File', '&Edit', '&View','&Navigate',
                     '&Code', '&Refactor', 'R&un', '&Tools']
        for item in menu_item:
            main_menu.addMenu(item)


class MultiChannelsPyQtGraph(QWidget):
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

        # Init the timer
        self.timer = QtCore.QTimer()

        self.init_win()

    def init_win(self):
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        # Compose tabs
        self.create_tab1()
        self.create_tab2()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    def create_tab1(self):
        self.tab1.layout = QGridLayout(self)
        # Create the plots
        self.init_eeg_plot()
        self.init_fft_plot()
        # # assign pushButton
        self.assign_n_to_ch()
        self.assign_action_to_ch()

        # self.pb2 = QPushButton("pb2")
        # self.pb3 = QPushButton("pb3")
        # self.pb4 = QPushButton("pb4")
        # self.tab2.layout.addWidget(self.pb2, 3, 0, 1, 1)
        # self.tab2.layout.addWidget(self.pb3, 4, 0, 1, 1)
        # self.tab2.layout.addWidget(self.pb4, 5, 0, 1, 1)
        self.tab1.setLayout(self.tab1.layout)

    def create_tab2(self):
        pass

    def assign_n_to_ch(self):
        for ch in range(self.N_CH):
            b_on_off_ch = QtGui.QPushButton(str(ch))
            style = ('QPushButton {background-color'
                                + ': {color}; '.format(color=self.button_color[ch])
                                + 'min-width: 14px}')
            b_on_off_ch.setStyleSheet(style)
            row = ch*3+2
            col = 0
            rowspan = 1
            self.tab1.layout.addWidget(b_on_off_ch, row, col, rowspan, 1)

    def assign_action_to_ch(self):
        for ch in range(self.N_CH):
            for b_n in range(self.BUTTON_PER_CH):
                b_action_ch = QtGui.QPushButton('act ' + str(ch*3 + b_n))
                b_action_ch.clicked.connect(self.print_allo)
                row = ch*3 + b_n + 1
                col = 2
                rowspan = 1
                self.tab1.layout.addWidget(b_action_ch, row, col, rowspan, 1)

    def print_allo(self):
        print('allo les dudddes ... ')

    def init_eeg_plot(self):
        """
        """
        for ch in range(self.N_CH):
            self.eeg_plot = pg.PlotWidget(background=(3, 3, 3))
            self.eeg_plot.plotItem.showGrid(x=True, y=True, alpha=0.1)
            # Add the label only for the last channel as they all have the same
            if ch == 7:
                self.eeg_plot.plotItem.setLabel(axis='bottom', text='Time', units='s')  # Todo : ALEXM : verifier l'uniter
                self.eeg_plot.plotItem.setLabel(axis='left', text='Amplitude', units='v')
            # Add the widget to the layout at the proper position
            row = ch*3+1
            col = 1
            rowspan = 3
            self.tab1.layout.addWidget(self.eeg_plot, row, col, rowspan, 1)

            self.eeg_plots.append(EEG_graph(self.eeg_plot, self.data_queue[ch],
                                            self.n_data_created,
                                            self.pen_color[ch]))
            self.timer.timeout.connect(self.eeg_plots[ch].update_eeg_plotting)

    def init_fft_plot(self):
        """
        """
        # Create the plot widget and its characteristics
        self.fft_plot = pg.PlotWidget(background=(3, 3, 3))
        self.fft_plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        self.fft_plot.plotItem.setLabel(axis='bottom', text='Frequency', units='Hz')   # Todo : ALEXM : verifier l'uniter
        self.fft_plot.plotItem.setLabel(axis='left', text='Amplitude', units='None')
        row = 1
        col = 3
        rowspan = 24
        # Add to tab layout
        self.tab1.layout.addWidget(self.fft_plot, row, col, rowspan, 1)
        # Associate the plot to an FFT_graph object
        self.fft_plot = FFT_graph(self.fft_plot, self.data_queue, self.n_data_created,
                                  self.pen_color)
        self.timer.timeout.connect(self.fft_plot.update_fft_plotting)

    def start_timer(self):
        self.timer.start(0)
