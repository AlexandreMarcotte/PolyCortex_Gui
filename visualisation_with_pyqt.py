# -*- coding: utf-8 -*-

# PLOTING the EEG data
from functools import partial
# Graph the data
from PyQt5.QtWidgets import *
    # (QLineEdit, QSlider, QPushButton, QVBoxLayout, QApplication, QWidget,
    #  QLabel, QCheckBox, QRadioButton,QTextEdit, QHBoxLayout, QFileDialog,
    #  QAction, qApp, QMainWindow, QMenuBar, QSlider, QGridLayout, QTabWidget)
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
from generated_signal import (stream_data_from_OpenBCI, CreateData,
                              CreateDataFromFile, read_data_from_file)
from save_to_file import WriteDataToFile


class App(QMainWindow):

    def __init__(self, data_queue, t_queue, t_init, n_data_created):
        super(App, self).__init__()
        self.setWindowTitle('--OpenBCI graph--')
        # Add a menu bar
        self.create_menu_bar()
        # message at the bottom
        self.statusBar().showMessage('Running the experiment ...')

        self.simple_graph = MultiChannelsPyQtGraph(data_queue, t_queue,
                                                   t_init, n_data_created)     # TODO: ALEXM divide this part in many objects
        self.setCentralWidget(self.simple_graph)

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
        self.N_BUTTON_PER_CH = 2
        # Contain all the button for all the channels with the specif action
        # they trigger
        self.action_button_func = []

        self.n_data_created = n_data_created
        self.N_CH = len(self.data_queue)
        self.eeg_plots = []

        # Openbci
        self.stream_from_board = False

        # P300 experiment
        self.p300_char = ['A', 'B', 'C', 'D', 'E', 'F',
                          'G', 'H', 'I', 'J', 'K', 'L',
                          'M', 'N', 'O', 'P', 'Q', 'R',
                          'S', 'T', 'U', 'V', 'W', 'X',
                          'Y', 'Z', '1', '2', '3', '4',
                          '5', '6', '7', '8', '9', '_']
        self.show_p300 = True

        # Init the timer
        self.timer_eeg = QtCore.QTimer()
        self.timer_fft = QtCore.QTimer()
        self.timer_p300 = QtCore.QTimer()

        self.init_font()

        self.init_win()

    def init_font(self):
        self.font = QtGui.QFont()
        self.font.setPointSize(50)

    def init_win(self):
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "EEG & FFT live graph")
        self.tabs.addTab(self.tab2, "P300 experiment")
        self.tabs.addTab(self.tab3, "EEG static graph")

        # Compose tabs
        self.create_tab1()
        self.create_tab2()
        self.create_tab3()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def init_saving(self):
        # write data to file:
        lock = threading.Lock()
        self.write_data_to_file = WriteDataToFile(self.data_queue,
                                             self.n_data_created, lock)
        self.write_data_to_file.start()

    def create_tab1(self):
        self.tab1.layout = QGridLayout(self)
        # Create the plots
        self.init_eeg_plot()
        self.init_fft_plot()
        # assign pushButton
        self.start_openbci_button()
        self.stop_openbci_button()
        self.assign_n_to_ch()
        self.assign_action_to_ch()

        self.tab1.setLayout(self.tab1.layout)

    def create_tab2(self):
        self.DARK_GREY = '#585858'  # (88, 88, 88)
        self.LIGHT_GREY = '#C8C8C8'  # (200, 200, 200)

        self.tab2.layout = QGridLayout(self)

        self.p300_plot = self.instantiate_p300_plot()
        row=1; col=0; rowspan=1; colspan=2
        self.tab2.layout.addWidget(self.p300_plot, row, col, rowspan, colspan)

        # start and stop button
        self.start_p300_button()
        self.stop_p300_button()

        self.timer_p300.timeout.connect(self.update_p300)

        self.tab2.setLayout(self.tab2.layout)

    def create_tab3(self):
        self.tab3.layout = QGridLayout(self)

        self.create_stationnary_plot()

        self.tab3.setLayout(self.tab3.layout)

    def create_stationnary_plot(self):
        # Read data from file
        # self.data = np.random.random(size=1000)
        self.data = read_data_from_file('csv_eeg_data.csv', n_ch=8)

        self.static_graph_update = []

        for graph_num, graph_data  in enumerate(self.data):
            # Instanciate the plot containing the crosshair
            self.crosshair_plot = pg.PlotWidget()
            # Instanciate the plot containing all the data
            self.all_data_plot = pg.PlotWidget()

            row=graph_num; col=0; rowspan=1; colspan=1
            self.tab3.layout.addWidget(self.crosshair_plot, row,
                                       col, rowspan, colspan)
            row=graph_num; col=1; rowspan=1; colspan=1
            self.tab3.layout.addWidget(self.all_data_plot, row,
                                       col, rowspan, colspan)

            # Label that show the position of the cross hair
            # self.label = pg.LabelItem()
            # self.crosshair_plot.addItem(self.label)
            # self.label.setText('Cross hair position')

            # Region of selection in the 'all_data_plot'
            self.region = pg.LinearRegionItem()

            # Tell the ViewBox to exclude this item when doing auto-range calculations.
            self.all_data_plot.addItem(self.region, ignoreBounds=True)
            self.crosshair_plot.setAutoVisible(y=True)

            self.crosshair_plot.plot(graph_data, pen="g")
            self.all_data_plot.plot(graph_data, pen="w")

            # Create 8 update function object, one for every plot
            self.static_graph_update.append(
                StaticGraphUpdate(self.region, self.crosshair_plot))

            # Connect all the update functions
            self.region.sigRegionChanged.connect(
                self.static_graph_update[graph_num].update_cross_hair_plot_range)

            self.crosshair_plot.sigRangeChanged.connect(
                self.static_graph_update[graph_num].update_region)

            # Set the starting position of the region
            self.region.setRegion([0, 200])

        # Create the cross hair and add it to the window
        # self.vLine = pg.InfiniteLine(angle=90, movable=False)
        # self.hLine = pg.InfiniteLine(angle=0, movable=False)
        # self.crosshair_plot.addItem(self.vLine, ignoreBounds=True)
        # self.crosshair_plot.addItem(self.hLine, ignoreBounds=True)

        # proxy = pg.SignalProxy(self.crosshair_plot.scene().sigMouseMoved,
        #                        rateLimit=60, slot=self.mouse_mouved)

    # ------------ P300 -------------
    def instantiate_p300_plot(self):
        p300_plot = pg.PlotWidget()
        p300_plot.setXRange(-2, 7)
        p300_plot.setYRange(-1, 5)
        p300_plot.hideAxis('bottom')
        p300_plot.hideAxis('left')
        return p300_plot

    def update_p300(self):
        rand_row = randint(0, 5)
        rand_col = randint(0, 5)
        # clear the widget on the screen at every display to add a new batch
        self.p300_plot.clear()
        # Add all number to the plot
        for no, one_char in enumerate(self.p300_char):
            col = no % 6
            row = no // 6
            # Change the color on the row and column selected from the random
            if rand_col == col or rand_row == row:
                char_color = '#F00'
            else:
                char_color = '#00F'

            char = pg.TextItem(fill=(0, 0, 0), anchor=(0.5,0))
            html = """<span style="color: {char_color};
                       font-size: 56pt; ">
                       {p300_char}""".format(char_color=char_color,
                                             p300_char=one_char)
            char.setHtml(html)

            self.p300_plot.addItem(char)
            char.setPos(col, row)

    def start_p300_button(self):
        b_start = QtGui.QPushButton('START_P300')
        b_start.clicked.connect(partial(self.start_p300))
        row=0; col=0; rowspan=1; colspan=1
        self.tab2.layout.addWidget(b_start, row, col, rowspan, colspan)

    @pyqtSlot()
    def start_p300(self):
        self.timer_p300.start(100)

    def stop_p300_button(self):
        b_stop = QtGui.QPushButton('STOP_P300')
        b_stop.clicked.connect(partial(self.stop_p300))
        row = 0; col = 1; rowspan = 1; colspan = 1
        self.tab2.layout.addWidget(b_stop, row, col, rowspan, colspan)

    @pyqtSlot()
    def stop_p300(self):
        self.timer_p300.stop()

    # ------------ P300  END -------------

    # ------------ OPENBCI ----------------
    def start_openbci_button(self):
        b_start = QtGui.QPushButton('START_OPENBCI')
        b_start.clicked.connect(partial(self.start_OpenBCI))
        row = 0; col = 1; rowspan = 1
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
        b_stop = QtGui.QPushButton('STOP_OPENBCI')
        b_stop.clicked.connect(partial(self.stop_OpenBCI))
        row = 0; col = 3; rowspan = 1
        self.tab1.layout.addWidget(b_stop, row, col, rowspan, 1)

    @pyqtSlot()
    def stop_OpenBCI(self):
        if self.stream_from_board:
            self.board.stop()
        self.stop_openbci_timer()
        # Stop saving process
        # self.write_data_to_file.join()                                       # TODO: ALEXM find a way to stop the saving when we stop the visualization of the data

    def start_openbci_timer(self):
        self.timer_eeg.start(0)
        self.timer_fft.start(500)

    def stop_openbci_timer(self):
        self.timer_eeg.stop()
        self.timer_fft.stop()

    def assign_n_to_ch(self):
        for ch in range(self.N_CH):
            # +1 so the number str start at 1
            b_on_off_ch = QtGui.QPushButton(str(ch + 1))
            style = ('QPushButton {background-color'
                                + ': {color}; '.format(color=self.button_color[ch])
                                + 'min-width: 14px}')
            b_on_off_ch.setStyleSheet(style)
            b_on_off_ch.clicked.connect(partial(self.stop_ch, ch))
            # Set position and size of the button values
            row = ch*3+2; col = 0; rowspan = 1
            self.tab1.layout.addWidget(b_on_off_ch, row, col, rowspan, 1)

    @pyqtSlot()
    def stop_ch(self, ch):
        for _ in range(500):
            self.data_queue[ch].append(0)

    def assign_action_to_ch(self):
        for ch in range(self.N_CH):
            for b_n in range(self.N_BUTTON_PER_CH):
                # Show an horizontale line at the average of the signal
                if b_n % self.N_BUTTON_PER_CH == 0:
                    b = QtGui.QPushButton('avg')
                    # b.clicked.connect(partial(self.show_avg, ch, 10))
                elif b_n % self.N_BUTTON_PER_CH == 1:
                    b = QtGui.QPushButton('max')
                    # b.clicked.connect(partial())

                # Set position and size of the button values
                row = ch*3 + b_n + 2  # +2 because there are two rows of b before
                col = 2; rowspan = 1
                self.tab1.layout.addWidget(b, row, col, rowspan, 1)

            # Add a vertical line to delimitate the action for each channel
            row = ch * 3 + 2 + 2; col = 2; rowspan = 1
            self.line = QFrame(self)
            self.line.setGeometry(QtCore.QRect())
            self.line.setFrameShape(QFrame.HLine)
            self.line.setFrameShadow(QFrame.Sunken)
            self.tab1.layout.addWidget(self.line, row, col, rowspan, 1)

    @pyqtSlot()
    def create_pulse(self, ch, intensity):
        self.data_queue[ch].append(intensity)

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
                rowspan = 3
            else:
                self.eeg_plot.plotItem.hideAxis('bottom')
                rowspan = 3
            # Add the widget to the layout at the proper position
            row = ch*3+1 + 1; col = 1

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
        self.fft_plot.plotItem.setLabel(axis='bottom', text='Frequency',
                                        units='Hz')                            # Todo : ALEXM : verifier l'uniter
        self.fft_plot.plotItem.setLabel(axis='left', text='Amplitude',
                                        units='None')
        row = 1 + 1; col = 3; rowspan = 24
        # Add to tab layout
        self.tab1.layout.addWidget(self.fft_plot, row, col, rowspan, 1)
        # Associate the plot to an FFT_graph object
        self.fft_plot = FFT_graph(self.fft_plot, self.data_queue, self.t_queue,
                                  self.n_data_created, self.pen_color)
        self.timer_fft.timeout.connect(self.fft_plot.update_fft_plotting)


class StaticGraphUpdate(object): 
    def __init__(self, region, crosshair_plot):
        self.region = region
        self.crosshair_plot = crosshair_plot
    
    def update_region(self, window, viewRange):
        """ Update the range of the region"""
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def update_cross_hair_plot_range(self):
        """ Update the cross_hair_plot range based on the region position """
        minX, maxX = self.region.getRegion()
        self.crosshair_plot.setXRange(minX, maxX, padding=0)

    # def mouse_mouved(evt):                                                   # Todo ALEXM try to make the cross hair move later
    #     pos = evt[0]  # select the x position of the mouse
    #     # if the mouse is inside the cross_hair_plot delimited region
    #     print('POS', pos, 'crosshair', self.crosshair_plot.sceneBoundingRect())
    #     if self.crosshair_plot.sceneBoundingRect().contains(pos):
    #         mousePoint = self.crosshair_plot.vb.mapSceneToView(pos)
    #         index = int(mousePoint.x())
    #         # print(index)
    #         # if index > 0 and index < len(self.data1):
    #         #     self.label.setText("""<span style='font-size: 12pt'>x=%0.1f,
    #         #                      <span style='color: green'>y2=%0.1f</span>"""\
    #         #                      % (mousePoint.x(), self.data2[index]))
    #         # Set the crosshair where on the mouse position
    #         self.vLine.setPos(mousePoint.x())
    #         self.hLine.setPos(mousePoint.y())


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