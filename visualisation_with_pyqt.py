# -*- coding: utf-8 -*-

# PLOTING the EEG data
from functools import partial
# Graph the data
from PyQt5.QtWidgets import \
    (QLineEdit, QSlider, QPushButton, QVBoxLayout, QApplication, QWidget,
     QLabel, QCheckBox, QRadioButton,QTextEdit, QHBoxLayout, QFileDialog,
     QAction, qApp, QMainWindow, QMenuBar, QSlider, QGridLayout, QTabWidget)
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap

# from pyqtgraph.Qt import QtGui
import numpy as np
import pyqtgraph as pg
from collections import deque
import threading
from numpy.fft import fft, fftfreq
import sched, time
import sys
from random import randint
# My packages
from frequency_counter import FrequencyCounter


class App(QMainWindow):

    def __init__(self, data_queue, t_queue, t_init, n_data_created):
        super().__init__()
        self.setWindowTitle('basic graph')
        # Add a menu bar
        self.create_menu_bar()
        # message at the bottom
        self.statusBar().showMessage('Running the experiment.')

        self.simple_graph = MultiChannelsPyQtGraph(data_queue, t_queue,
                                                   t_init, n_data_created)
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
    def __init__(self, data_queue, t_queue, t_init, n_data_created):
        """
        """
        super(MultiChannelsPyQtGraph, self).__init__()
        self.data_queue = data_queue
        self.t_queue = t_queue
        self.t_init = t_init
        self.pen_color = ['r', 'y', 'g', 'c', 'b', 'm', (100, 100, 100), 'w']
        self.button_color = ['red', 'yellow', 'green', 'cyan',
                             'blue', 'magenta', 'grey', 'white']
        self.BUTTON_PER_CH = 2
        # Contain all the button for all the channels with the specif action
        # they trigger
        self.action_button_func = []

        self.n_data_created = n_data_created
        self.N_CH = len(self.data_queue)
        self.eeg_plots = []

        # P300 experiment
        self.char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                     'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']

        # Init the timer
        self.timer_eeg = QtCore.QTimer()
        self.timer_fft = QtCore.QTimer()
        self.timer_p300 = QtCore.QTimer()

        self.init_font()

        self.init_win()

    def init_font(self):
        self.font = QtGui.QFont()
        self.font.setFamily('FreeMono')
        self.font.setBold(True)
        self.font.setPointSize(50)

    def init_win(self):
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "EEG & FFT")
        self.tabs.addTab(self.tab2, "P300 experiment")

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

        self.tab1.setLayout(self.tab1.layout)

    def create_tab2(self):
        self.DARK_GREY = '#585858'  # (88, 88, 88)
        self.LIGHT_GREY = '#C8C8C8'  # (200, 200, 200)
        self.tab2.layout = QGridLayout(self)
        self.timer_p300.timeout.connect(self.update_p300)

    def update_p300(self):
        # Select a new random position for the cross
        rand_h = randint(0, 5)
        rand_v = randint(0, 5)
        # Draw all characters
        for i, c in enumerate(self.char):
            pos_v = i//6
            pos_h = i%6
            text = QLabel(c)
            text.setFont(self.font)
            # Put lighter color on the selected cross
            if pos_h == rand_h or pos_v == rand_v:
                color = self.LIGHT_GREY
            else:
                color = self.DARK_GREY
            style = ('QLabel { color : ' + '{color}'.format(color=color) + ' }')
            text.setStyleSheet(style)
            self.tab2.layout.addWidget(text, pos_v, pos_h, 1, 1)

        self.tab2.setLayout(self.tab2.layout)

    def assign_n_to_ch(self):
        for ch in range(self.N_CH):
            b_on_off_ch = QtGui.QPushButton(str(ch))
            style = ('QPushButton {background-color'
                                + ': {color}; '.format(color=self.button_color[ch])
                                + 'min-width: 14px}')
            b_on_off_ch.setStyleSheet(style)
            b_on_off_ch.clicked.connect(partial(self.stop_ch, ch))
            # Set position and size of the button values
            row = ch*3+2; col = 0; rowspan = 1
            self.tab1.layout.addWidget(b_on_off_ch, row, col, rowspan, 1)

    def assign_action_to_ch(self):
        for ch in range(self.N_CH):
            for b_n in range(self.BUTTON_PER_CH):
                b = QtGui.QPushButton('A' + str(ch*3 + b_n))
                b.clicked.connect(partial(self.create_pulse, ch, 10))
                # Set position and size of the button values
                row = ch*3 + b_n + 1; col = 2; rowspan = 1
                self.tab1.layout.addWidget(b, row, col, rowspan, 1)

    @pyqtSlot()
    def create_pulse(self, ch, intensity):
        self.data_queue[ch].append(intensity)

    @pyqtSlot()
    def stop_ch(self, ch):
        for _ in range(500):
            self.data_queue[ch].append(0)

    def init_eeg_plot(self):
        """
        """
        for ch in range(self.N_CH):
            self.eeg_plot = pg.PlotWidget(background=(3, 3, 3))
            self.eeg_plot.plotItem.showGrid(x=True, y=True, alpha=0.1)
            # Add the label only for the last channel as they all have the same
            self.eeg_plot.plotItem.setLabel(axis='left', units='v')
            if ch == 7:
                self.eeg_plot.plotItem.setLabel(axis='bottom', text='Time',
                                                units='s')                      # Todo : ALEXM : verifier l'uniter
                rowspan = 10
            else:
                self.eeg_plot.plotItem.hideAxis('bottom')
                rowspan = 3
            # Add the widget to the layout at the proper position
            row = ch*3+1
            col = 1

            self.tab1.layout.addWidget(self.eeg_plot, row, col, rowspan, 1)

            self.eeg_plots.append(EEG_graph(self.eeg_plot, self.data_queue[ch],
                                            self.t_queue, self.t_init,
                                            self.n_data_created,
                                            self.pen_color[ch]))
            self.timer_eeg.timeout.connect(self.eeg_plots[ch].update_eeg_plotting)

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
        self.fft_plot = FFT_graph(self.fft_plot, self.data_queue, self.t_queue,
                                  self.n_data_created, self.pen_color)
        self.timer_fft.timeout.connect(self.fft_plot.update_fft_plotting)

    def start_timer(self):
        self.timer_eeg.start(0)
        self.timer_fft.start(500)
        self.timer_p300.start(700)




class EEG_graph(object):
    """
    """
    def __init__(self, eeg_plot, one_ch_deque, t_queue, t_init,
                 n_data_created, pen_color):
        self.one_ch_deque = one_ch_deque
        self.t_queue = t_queue
        self.t_init = t_init
        self.n_data_created = n_data_created[0]

        self.N_DATA = len(one_ch_deque)
        self.curve_eeg = eeg_plot.plot(self.t_queue, deque(np.zeros(self.N_DATA),
                                       maxlen=self.N_DATA))
        self.curve_eeg.setPen(pen_color)

    def update_eeg_plotting(self):
        self.curve_eeg.setData(self.t_queue, self.one_ch_deque)


class FFT_graph(object):
    """
    """
    def __init__(self, freq_plot, data_queue, t_queue, n_data_created, pen_color):
        self.data_queue = data_queue
        self.t_queue = t_queue
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
        # interval of time from the first to the last value that was add to the queue
        delta_t = (self.t_queue[-1] - self.t_queue[0])
        # Calculate FFT
        freq_range = np.linspace(0, self.N_DATA//2/delta_t, self.N_DATA//2)

        for ch in range(self.N_CH):
            ch_fft = fft(self.data_queue[ch])
            # Keep all frequency possibles                                                  # TODO: Change frequency in function of time
            self.curve_freq[ch].setData(freq_range, abs(ch_fft[:len(ch_fft) // 2]))         # TODO: ALEXM prendre abs ou real? avec real il y a des valeurs negatives est-ce que c'est normal?
            self.curve_freq[ch].setPen(self.pen_color[ch])





# class P300(MultiChannelsPyQtGraph):
#     def __init__(self, data_queue, n_data_created):
#         super(P300, self).__init__(data_queue, n_data_created)
#         self.init_font()
#         self.char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
#                      'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
#                      'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']
#         DARK_GREY = '#585858'  # (88, 88, 88)
#         LIGHT_GREY = '#C8C8C8'  # (200, 200, 200)
#
#         rand_h = randint(0, 5)
#         rand_v = randint(0, 5)
#
#         # Draw all characters
#         for i, c in enumerate(self.char):
#             pos_v = i//6
#             pos_h = i%6
#             text = QLabel(c)
#             text.setFont(self.font)
#             if pos_h == rand_h or pos_v == rand_v:
#                 color = LIGHT_GREY
#             else:
#                 color = DARK_GREY
#             style = ('QLabel { color : ' + '{color}'.format(color=color) + ' }')
#             text.setStyleSheet(style)
#             self.tab2.layout.addWidget(text, pos_v, pos_h, 1, 1)
#
#         self.tab2.setLayout(self.tab2.layout)
#
#     def init_font(self):
#         self.font = QtGui.QFont()
#         self.font.setFamily('FreeMono')
#         self.font.setBold(True)
#         self.font.setPointSize(50)

    # def update(self):