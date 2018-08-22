# -*- coding: utf-8 -*-

# -- General packages --
# # Graph the data
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot

import pyqtgraph as pg

from functools import partial
from collections import deque
import numpy as np
import threading
from numpy.fft import fft, fftfreq

# -- My packages --
from generated_signal import (stream_data_from_OpenBCI, CreateData,
                              CreateDataFromFile)
from save_to_file import WriteDataToFile


class Tab1(object):
    def __init__(self, main_window, tab1, n_data_created, data_queue, t_queue,
                 t_init):
        self.main_window = main_window
        self.tab1 = tab1
        self.t_queue = t_queue
        self.t_init = t_init

        self.pen_color = ['r', 'y', 'g', 'c', 'b', 'm', (100, 100, 100), 'w']
        self.button_color = ['red', 'yellow', 'green', 'cyan',
                             'blue', 'magenta', 'grey', 'white']
        self.N_BUTTON_PER_CH = 2
        # Contain all the button for all the channels with the specif action
        # they trigger
        self.action_button_func = []

        self.n_data_created = n_data_created
        self.data_queue = data_queue
        self.N_CH = len(self.data_queue)
        self.eeg_plots = []

        # Openbci
        self.stream_from_board = False
        self.save_path = 'csv_eeg_data.csv'

        # Buttons action
        self.action_buttons = []
        # # Create timer
        self.timer_avg = QtCore.QTimer()
        self.timer_avg = QtCore.QTimer()
        # Init the timer
        self.timers_eeg = []
        for _ in range(self.N_CH):
            self.timers_eeg.append(QtCore.QTimer())
        self.timer_fft = QtCore.QTimer()

    def create_tab1(self):
        self.tab1.layout = QGridLayout(self.main_window)
        # Create the plots
        self.init_eeg_plot()
        self.init_fft_plot()
        # assign pushButton
        self.start_openbci_button()
        self.stop_openbci_button()
        self.save_data_to_file()
        self.assign_n_to_ch()
        self.assign_action_to_ch()

        self.tab1.setLayout(self.tab1.layout)

    def start_openbci_button(self):
        b_start = QtGui.QPushButton('Start Data Stream')
        b_start.setStyleSheet("background-color: rgba(0, 100, 0, 0.5)")
        b_start.clicked.connect(partial(self.start_OpenBCI))
        row=0; col=1; rowspan=1
        self.tab1.layout.addWidget(b_start, row, col, rowspan, 1)

    @pyqtSlot()
    def start_OpenBCI(self):
        # -----Start streaming data from the OPENBCI board ------
        if self.stream_from_board:
            self.board = stream_data_from_OpenBCI(self.data_queue, self.t_queue,
                                                  self.t_init,
                                                  self.n_data_created)
        else:
            # Create fake data for test case
            create_data = CreateData(self.data_queue, self.t_queue,
                                     self.t_init, self.n_data_created)
            create_data.start()
            # create_data = CreateDataFromFile(self.data_queue, self.t_queue,
            #                                  self.t_init, self.n_data_created)
            # create_data.start()
        self.start_openbci_timer()
        # SAVE the data received to file
        self.init_saving()

    def stop_openbci_button(self):
        b_stop = QtGui.QPushButton('Stop Data Stream')
        b_stop.setStyleSheet("background-color: rgba(100, 0, 0, 0.5)")
        b_stop.clicked.connect(partial(self.stop_OpenBCI))
        row=0; col=4; rowspan=1
        self.tab1.layout.addWidget(b_stop, row, col, rowspan, 1)

    @pyqtSlot()
    def stop_OpenBCI(self):
        if self.stream_from_board:
            self.board.stop()
        self.stop_openbci_timer()
        # Stop saving process
        # self.write_data_to_file.join()                                       # TODO: ALEXM find a way to stop the saving when we stop the visualization of the data

    def save_data_to_file(self):
        # Create button to open date file
        open_file = QtGui.QPushButton('Save Data')
        open_file.setStyleSheet("background-color: rgba(0, 0, 0, 0.4)")

        row=26; col=1; rowspan=1; colspan=1
        self.tab1.layout.addWidget(open_file, row, col, rowspan, colspan)
        # Create text box to show or enter path to data file
        self.data_path = QtGui.QLineEdit('csv_eeg_data.csv')
        row=26; col=4; rowspan=1; colspan=3
        self.tab1.layout.addWidget(self.data_path, row, col, rowspan, colspan)

    def start_openbci_timer(self):
        for timer in self.timers_eeg:
            timer.start(0)
        self.timer_fft.start(2000)

    def stop_openbci_timer(self):
        for timer in self.timers_eeg:
            timer.stop()
        self.timer_fft.stop()

    def assign_n_to_ch(self):
        for ch in range(self.N_CH):
            # +1 so the number str start at 1
            b_on_off_ch = QtGui.QPushButton(str(ch + 1))
            b_on_off_ch.setCheckable(True)
            style = ('QPushButton {background-color'
                     + ': {color}; '.format(color=self.button_color[ch])
                     + 'min-width: 14px}')
            b_on_off_ch.setStyleSheet(style)
            ch_number_action = ChNumberAction(self.timers_eeg, ch)
            b_on_off_ch.toggled.connect(partial(ch_number_action.stop_ch))
            # Set position and size of the button values
            row=ch * 3 + 2; col=0; rowspan=1
            self.tab1.layout.addWidget(b_on_off_ch, row, col, rowspan, 1)

    def assign_action_to_ch(self):
        pos = 2  # Start the position at two because the buttons start on the second row
        tot_b_num = 0
        for ch in range(self.N_CH):
            for b_n in range(self.N_BUTTON_PER_CH):
                # Create an action object and add it to the list of all actions
                # in the tab
                action_button = ActionButton(self.data_queue, self.tab1,
                                             b_n, ch, pos)
                self.action_buttons.append(action_button)
                # Average
                if b_n % self.N_BUTTON_PER_CH == 0:
                    # Create an average action
                    b = QtGui.QPushButton('avg')  # TODO: ALEXM remove redondancy
                    b.setStyleSheet("background-color: rgba(5, 5, 5, 0.3)")
                    b.setCheckable(True)
                    b.clicked.connect(partial(self.show_avg,
                                              self.action_buttons[tot_b_num]))
                # Max
                elif b_n % self.N_BUTTON_PER_CH == 1:
                    # Create a max action
                    b = QtGui.QPushButton('max')
                    b.setStyleSheet("background-color: rgba(5, 5, 5, 0.3)")
                    b.setCheckable(True)
                    b.clicked.connect(partial(self.show_max,
                                              self.action_buttons[tot_b_num]))
                # Set position and size of the button values
                row=pos
                col=2; rowspan=1; colspan=1
                self.tab1.layout.addWidget(b, row, col, rowspan, colspan)
                pos += 1
                # Change the total number of buttons
                tot_b_num += 1

            # Add a vertical line to delineate the action for each channel
            row = pos; col = 2; rowspan = 1; colspan = 1
            self.line = QFrame(self.main_window)
            self.line.setGeometry(QtCore.QRect())
            self.line.setFrameShape(QFrame.HLine)
            self.line.setFrameShadow(QFrame.Sunken)
            self.tab1.layout.addWidget(self.line, row, col, rowspan, colspan)
            pos += 1

    @pyqtSlot()  # TODO: ALEXM remove this duplicate
    def show_avg(self, action_buttons):
        # Update the average label
        self.timer_avg.timeout.connect(action_buttons.update_avg)
        self.timer_avg.start(600)

    @pyqtSlot()
    def show_max(self, action_button):
        # Update the average label
        self.timer_avg.timeout.connect(action_button.update_max)
        self.timer_avg.start(600)

    def init_fft_plot(self):
        """
        """
        # Create the plot widget and its characteristics
        self.fft_plot = pg.PlotWidget(background=(3, 3, 3))
        self.fft_plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        self.fft_plot.plotItem.setLabel(axis='bottom', text='Frequency',
                                        units='Hz')  # Todo : ALEXM : verifier l'uniter
        self.fft_plot.plotItem.setLabel(axis='left', text='Amplitude',
                                        units='None')
        row=1 + 1; col=4; rowspan=24
        # Add to tab layout
        self.tab1.layout.addWidget(self.fft_plot, row, col, rowspan, 1)
        # Associate the plot to an FFT_graph object
        self.fft_plot = FFT_graph(self.fft_plot, self.data_queue, self.t_queue,
                                  self.n_data_created, self.pen_color)
        self.timer_fft.timeout.connect(self.fft_plot.update_fft_plotting)

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
                                                units='s')  # Todo : ALEXM : verifier l'uniter
                rowspan = 3
            else:
                self.eeg_plot.plotItem.hideAxis('bottom')
                rowspan = 3
            # Add the widget to the layout at the proper position
            row=ch * 3 + 1 + 1; col=1

            self.tab1.layout.addWidget(self.eeg_plot, row, col, rowspan, 1)

            self.eeg_plots.append(EEG_graph(self.eeg_plot, self.data_queue[ch],
                                            self.t_queue, self.t_init,
                                            self.n_data_created,
                                            self.pen_color[ch]))
            self.timers_eeg[ch].timeout.connect(self.eeg_plots[ch].update_eeg_plotting)

    def init_saving(self):
        # write data to file:
        lock = threading.Lock()
        self.write_data_to_file = WriteDataToFile(self.data_queue,
                                                  self.n_data_created, lock)
        self.write_data_to_file.start()


class EEG_graph(object):
    """
    """
    def __init__(self, eeg_plot, one_ch_deque, t_queue, t_init,
                 n_data_created, pen_color):
        self.eeg_plot = eeg_plot
        self.one_ch_deque = one_ch_deque
        self.t_queue = t_queue
        self.t_init = t_init
        self.n_data_created = n_data_created[0]

        self.N_DATA = len(one_ch_deque)
        self.curve_eeg = self.eeg_plot.plot(self.t_queue,
                                            deque(np.zeros(self.N_DATA),
                                            maxlen=self.N_DATA))
        self.curve_eeg.setPen(pen_color)

    def update_eeg_plotting(self):
        # WARNING: When I plot with the time, the quality of the signal degrade
        self.curve_eeg.setData(self.t_queue, self.one_ch_deque)
        # self.curve_eeg.setData(self.one_ch_deque)
        # h_line = pg.InfiniteLine(angle=0, movable=False)
        # self.eeg_plot.addItem(h_line, ignoreBounds=True)

    def remove_ch_from_plotting(self):
        pass
        # This allows us to remove a ch from being plot
        # Je dois aussi arreter d'aller voir la channel sur le open bci:
        # Faire un timer par channel instead


class FFT_graph(object):
    """
    """
    def __init__(self, freq_plot, data_queue, t_queue, n_data_created,
                 pen_color):
        self.data_queue = data_queue
        self.t_queue = t_queue
        self.n_data_created = n_data_created
        self.freq_plot = freq_plot
        self.pen_color = pen_color

        self.N_DATA = len(self.data_queue[0])
        self.N_CH = len(self.data_queue)

        self.curve_freq = []
        for ch in range(self.N_CH):
            self.curve_freq.append(freq_plot.plot(deque(np.zeros(self.N_DATA),
                                                        maxlen=self.N_DATA)), )

    def update_fft_plotting(self):
        # interval of time from the first to the last value that was add to the queue
        delta_t = (self.t_queue[-1] - self.t_queue[0])
        # Calculate FFT (Remove freq 0 because it gives a really high value on the graph
        freq_range = np.linspace(1, self.N_DATA//2/delta_t, self.N_DATA//2 - 1)

        for ch in range(self.N_CH):
            ch_fft = fft(self.data_queue[ch])
            # Keep all frequency possibles                                                  # TODO: Change frequency in function of time
            self.curve_freq[ch].setData(freq_range, abs(ch_fft[1:self.N_DATA//2]))         # TODO: ALEXM prendre abs ou real? avec real il y a des valeurs negatives est-ce que c'est normal?
            self.curve_freq[ch].setPen(self.pen_color[ch])


class ChNumberAction(object):
    def __init__(self, timers_eeg, ch):
        self.timers_eeg = timers_eeg
        self.ch = ch

    @QtCore.pyqtSlot(bool)
    def stop_ch(self, checked):
        if checked:
            self.timers_eeg[self.ch].stop()
        else:
            self.timers_eeg[self.ch].start()


class ActionButton(object):
    def __init__(self, data_queue, tab, b_n, ch, pos):
        self.data_queue = data_queue
        self.b_n = b_n
        self.ch = ch
        self.tab = tab
        self.pos = pos

    def update_avg(self):                                                      # TODO: ALEXM eliminate duplicate of these two actions
        # Create the average label
        avg_label = QtGui.QLabel(
            f' : {np.round(np.average(self.data_queue[self.ch]), 2)} Vrms')
        # Set position of the label
        row = self.pos; col = 2; rowspan = 1; colspan = 1
        self.tab.layout.addWidget(avg_label, row, col + 1, rowspan, colspan)

    def update_max(self):
        # Create the average label
        avg_label = QtGui.QLabel(
            f' : {np.round(np.max(self.data_queue[self.ch]), 2)} Vrms')
        # Set position of the label
        row = self.pos; col = 2; rowspan = 1; colspan = 1
        self.tab.layout.addWidget(avg_label, row, col + 1, rowspan, colspan)