# -*- coding: utf-8 -*-
# -- General packages --
# # Graph the data
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot

import pyqtgraph as pg
from pyqtgraph.dockarea import *

from functools import partial
from collections import deque
import numpy as np
import threading
from numpy.fft import fft, fftfreq
import time
import datetime
import atexit
import math
import os
# Classification
from sklearn.externals import joblib
import matplotlib.pyplot as plt
from signal_manipulation import uniformize_data
from time import time

# -- My packages --
from generate_signal.generated_signal import (
    stream_data_from_OpenBCI, CreateData, CreateDataFromFile)
# from save_to_file import WriteDataToFile
# from visualisation_with_pyqt import MainWindow

class EegFftClassifTab:
    def __init__(self, main_window, tab_w, gv):
        super().__init__()
        self.main_window = main_window
        self.tab_w = tab_w
        self.gv = gv

        self.last_classified_type = [0]
        
        self.lock = threading.Lock()

        DEQUE_LEN = 1250
        self.zero_data_queue = deque(np.zeros(DEQUE_LEN), maxlen=DEQUE_LEN)

        self.pen_color = ['r', 'y', 'g', 'c', 'b', 'm',
                          (100, 100, 100), 'w', 'k']
        self.button_color = ['red', 'yellow', 'green', 'cyan',
                             'blue', 'magenta', 'grey', 'white']
        self.N_BUTTON_PER_CH = 4
        # Contain all the button for all the channels with the specif action
        # they trigger
        self.actn_btns_func = []

        # self.gv.n_data_created = n_data_created
        self.gv.N_CH = len(self.gv.data_queue)
        self.eeg_plots = []

        self.choose_file = None

        self.time = datetime.datetime.now()
        self.save_path = f'./csv_saved_files/2exp_pinch_close_{self.time}.csv'
        self.stream_path = f'./experiment_csv/2exp_pinch_close_2018-08-29 19:44:54.567417.csv'
        # Buttons action
        self.actn_btns = []
        # Init the timer
        self.init_timers()
        # Create the tab itself
        self.create_tab()

    def init_timers(self):
        # EEG timers
        self.timers_eeg = []
        for _ in range(self.gv.N_CH + 1):
            self.timers_eeg.append(QtCore.QTimer())
        # FFT timer
        self.timer_fft = QtCore.QTimer()
        # Classification timer
        self.timer_classif = QtCore.QTimer()

    def create_tab(self):
        self.tab_w.layout = QHBoxLayout(self.main_window)
        # Add docs to the tab
        self.area = DockArea()
        self.tab_w.layout.addWidget(self.area)
        self.create_docks()
        # Create the plots
        # - EEG
        self.init_eeg_plot()
        # - FFT
        self.init_fft_plot()
        self.fft_on_off_button()
        # - Wave plot
        self.init_wave_plot()
        self.init_show_classif_plot()
        self.wave_plot_on_off_button()
        # assign pushButton
        self.start_openbci_button()
        self.stop_openbci_button()
        self.save_data_to_file()
        self.assign_n_to_ch()
        self.assign_action_to_ch()
        # self.add_stream_combo_box(2)
        self.add_banner()

        self.tab_w.setLayout(self.tab_w.layout)

    def create_docks(self):
        # - EEG
        self.eeg_dock = Dock('EEG')
        self.area.addDock(self.eeg_dock, 'left')
        # Add the layout to the dock
        self.eeg_layout = pg.LayoutWidget()
        # Create scrolling region for portion graph
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.eeg_layout)
        self.eeg_dock.addWidget(self.scroll)
        # - FFT
        self.fft_dock = Dock('FFT', size=(5,10))
        self.area.addDock(self.fft_dock, 'right')
        self.fft_layout = pg.LayoutWidget()
        self.fft_dock.addWidget(self.fft_layout)
        # - Wave plot
        self.wave_dock = Dock('Wave', size=(5,10))
        self.area.addDock(self.wave_dock, 'bottom', self.fft_dock)
        self.wave_layout = pg.LayoutWidget()
        self.wave_dock.addWidget(self.wave_layout)
        # - Acceleration Dock
        self.show_classif_dock = Dock('Classification', size=(5, 10))
        self.area.addDock(self.show_classif_dock, 'below', self.wave_dock)
        self.show_classif_layout = pg.LayoutWidget()
        self.show_classif_dock.addWidget(self.show_classif_layout)
        # Make sure the wave is shown on top
        self.area.moveDock(self.wave_dock, 'above', self.show_classif_dock)
        # - Saving dock
        self.saving_dock = Dock('Saving', size=(1,1))
        self.saving_dock.hideTitleBar()
        self.area.addDock(self.saving_dock, 'bottom', self.eeg_dock)
        self.saving_layout = pg.LayoutWidget()
        self.saving_dock.addWidget(self.saving_layout)
        # - Banner dock
        self.banner_dock = Dock('Banner', size=(1, 1))
        self.banner_dock.hideTitleBar()
        self.area.addDock(self.banner_dock, 'bottom', self.wave_dock)
        self.banner_layout = pg.LayoutWidget()
        self.banner_dock.addWidget(self.banner_layout)

    def fft_on_off_button(self):
        b = QPushButton('Show FFT', self.main_window)
        b.setStyleSheet("background-color: rgba(0, 0, 80, 0.4)")
        row=0; col=0; rowspan=1; colspan=1
        self.fft_layout.addWidget(b, row, col, rowspan, colspan)
        b.setCheckable(True)
        b.toggled.connect(partial(self.start_fft))

    @QtCore.pyqtSlot(bool)
    def start_fft(self, checked):
        if checked:
            self.timer_fft.start(250)
        else:
            self.timer_fft.stop()

    def wave_plot_on_off_button(self):
        b = QPushButton('Show wave signal', self.main_window)
        b.setStyleSheet("background-color: rgba(0, 0, 80, 0.4)")
        row=0; col=0; rowspan=1; colspan=1
        self.wave_layout.addWidget(b, row, col, rowspan, colspan)

    def add_banner(self):
        # Polycortex
        polycortex_banner = QLabel(self.main_window)
        polycortex_banner.setPixmap(QtGui.QPixmap('./logo/polycortex_banner.png'))
        row=0; col=0; rowspan=1; colspan=1
        self.banner_layout.addWidget(polycortex_banner, row, col, rowspan, colspan)
        # OpenBci
        open_bci_banner = QLabel(self.main_window)
        open_bci_banner.setPixmap(QtGui.QPixmap('./logo/openbci_banner.png'))
        row=0; col=1; rowspan=1; colspan=1
        self.banner_layout.addWidget(open_bci_banner, row, col, rowspan, colspan)

    def add_choose_streaming_file_b(self):
        # Create button to open date file
        self.choose_file = QtGui.QPushButton('Choose streaming file')
        self.choose_file.setStyleSheet("background-color: rgba(0, 0, 100, 0.5)")
        self.choose_file.clicked.connect(partial(self.choose_streaming_file))
        row=0; col=1; rowspan=1; colspan=1
        self.stream_layout.addWidget(self.choose_file, row, col, rowspan, colspan)

    @pyqtSlot()
    def choose_streaming_file(self):
        # From: https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self.main_window, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            self.stream_path = file_name

    def start_openbci_button(self):
        b_start = QtGui.QPushButton('Start eeg stream')
        b_start.setStyleSheet("background-color: rgba(0, 100, 0, 0.5)")
        b_start.clicked.connect(partial(self.start_streaming_data))
        row=2; col=1; rowspan=1; colspan=1
        self.eeg_layout.addWidget(b_start, row, col, rowspan, colspan)

    @pyqtSlot()
    def start_streaming_data(self):
        # -----Start streaming data from OPENBCI board ------
        if self.gv.stream_origin[0] == 'Stream from OpenBCI':
            self.board = stream_data_from_OpenBCI(self.gv)
        elif self.gv.stream_origin[0] == 'Stream from fake data':
            # Create fake data for test case
            create_data = CreateData(self.gv)
            create_data.start()

        elif self.gv.stream_origin[0] == 'Stream from file':
            create_data = CreateDataFromFile(self.gv, self.stream_path)
            create_data.start()

        self.start_openbci_timer()
        # SAVE the data received to file
        self.save_path = self.save_path_line_edit.text()
        self.init_saving()

    def stop_openbci_button(self):
        b_stop = QtGui.QPushButton('Stop eeg stream')
        b_stop.setStyleSheet("background-color: rgba(100, 0, 0, 0.5)")
        b_stop.clicked.connect(partial(self.stop_OpenBCI))
        row=2; col=2; rowspan=1; colspan=1
        self.eeg_layout.addWidget(b_stop, row, col, rowspan, colspan)

    @pyqtSlot()
    def stop_OpenBCI(self):
        if self.gv.stream_origin[0] == 'Stream from OpenBCI':
            self.board.stop()
        self.stop_openbci_timer()
        # Stop saving process
        # self.write_data_to_file.join()                                       # TODO: ALEXM find a way to stop the saving when we stop the visualization of the data

    def save_data_to_file(self):
        # Create text box to show or enter path to data file
        self.save_path_line_edit = QtGui.QLineEdit(self.save_path)
        row=0; col=0; rowspan=1; colspan=2
        self.saving_layout.addWidget(self.save_path_line_edit, row, col, rowspan, colspan)
        # Create button to open date file
        open_file = QtGui.QPushButton('Choose saving directory')
        open_file.clicked.connect(partial(self.save_file_dialog))
        row=1; col=0; rowspan=1; colspan=1
        self.saving_layout.addWidget(open_file, row, col, rowspan, colspan)
        # Button to save all the current data that was generated
        self.save_cur_data_b = QtGui.QPushButton('Save data Now')
        row=1; col=1; rowspan=1; colspan=1
        self.saving_layout.addWidget(self.save_cur_data_b, row, col, rowspan, colspan)

    def save_file_dialog(self):
        # From: https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            self.main_window, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.save_path = file_name
            self.data_path_line_edit.setText(self.save_path)

    def write_to_file(self):
        print(f'Save data to file...')

        with open(self.save_path, 'w') as f:
            # Make sure all the queue in self.gv.all_data are the same length
            all_len = [len(d) for d in self.gv.all_data] + [len(self.gv.all_t)] \
                    + [len(self.gv.all_experiment_val)]
            print(all_len)
            min_len = min(all_len)
            # Remove extra data
            for i in range(len(self.gv.all_data)):
                if len(self.gv.all_data[i]) > min_len:
                    print('plus grand')
                    self.gv.all_data[i].pop()

            if len(self.gv.all_t) > min_len:
                self.gv.all_t.pop()

            if len(self.gv.all_experiment_val) > min_len:
                self.all_experiment_data.pop()

            # Create the proper dimension for the concatenation
            t_queue = np.array(self.gv.all_t)[None, :]
            experiment_queue = np.array(self.gv.all_experiment_val)[None, :]

            # Concatenate
            save_val = np.concatenate((self.gv.all_data, t_queue,
                                       experiment_queue))
            # Save
            np.savetxt(f, np.transpose(save_val), delimiter=',')

    def start_openbci_timer(self):
        # Start EEG timers
        for timer in self.timers_eeg:
            timer.start()
        # Start live classification
        self.timer_classif.start(0)

    def stop_openbci_timer(self):
        for timer in self.timers_eeg:
            timer.stop()

    def assign_n_to_ch(self):
        for ch in range(self.gv.N_CH):
            # +1 so the number str start at 1
            b_on_off_ch = QtGui.QPushButton(str(ch + 1))
            b_on_off_ch.setCheckable(True)
            b_on_off_ch.setToolTip('Stop current channel')
            style = ('QPushButton {background-color'
                     + ': {color}; '.format(color=self.button_color[ch])
                     + 'min-width: 14px}')
            b_on_off_ch.setStyleSheet(style)
            ch_number_action = ChNumberAction(self.timers_eeg, ch)
            b_on_off_ch.toggled.connect(partial(ch_number_action.stop_ch))
            # Set position and size of the button values
            row=ch*3+3; col=0; rowspan=1
            self.eeg_layout.addWidget(b_on_off_ch, row, col, rowspan, 1)

    def assign_action_to_ch(self):
        pos = 3  # Start the position at two because the buttons start on the second row
        tot_b_num = 0
        for ch in range(self.gv.N_CH):
            for b_n in range(self.N_BUTTON_PER_CH):
                # Create an action object and add it to the list of all actions
                # in the tab
                action_button = ActionButton(self.gv, self.eeg_layout,
                                             b_n, ch, pos)
                self.actn_btns.append(action_button)
                # Average
                if b_n % self.N_BUTTON_PER_CH == 0:
                    col = 3
                    b = self.create_actn_btn(
                        tot_b_num, 'A', tip='Show average value of queue')
                    b.toggled.connect(partial(self.actn_btns[tot_b_num].show_avg))

                # Max
                elif b_n % self.N_BUTTON_PER_CH == 1:
                    col = 3
                    # Create a max action
                    b = self.create_actn_btn(
                        tot_b_num, 'M', tip='Show max value of queue')
                    b.toggled.connect(partial(self.actn_btns[tot_b_num].show_max))

                # Detection
                elif b_n % self.N_BUTTON_PER_CH == 2:
                    pos-=2; col = 4
                    b = self.create_actn_btn(
                        tot_b_num, 'D', tip='Show detected class patern')
                # Other function
                elif b_n % self.N_BUTTON_PER_CH == 3:
                    col = 4
                    b = self.create_actn_btn(tot_b_num, 'O', 'Show other action')
                # Set position and size of the button values
                row=pos; rowspan=1; colspan=1
                self.eeg_layout.addWidget(b, row, col, rowspan, colspan)
                pos += 1
                # Change the total number of buttons
                tot_b_num += 1

            # Add a vertical line to delineate the action for each channel
            row=pos; col=3; rowspan=1; colspan=2
            self.line = QFrame(self.main_window)
            self.line.setGeometry(QtCore.QRect())
            self.line.setFrameShape(QFrame.HLine)
            # self.line.setFrameShadow(QFrame.Sunken)
            self.eeg_layout.addWidget(self.line, row, col, rowspan, colspan)
            pos += 1
    
    def create_actn_btn(self, tot_b_num, actn_letter, actn_func=None,
                        tip='', checkable=True):
        b = QtGui.QPushButton(actn_letter)
        b.setToolTip(tip)
        b.setCheckable(checkable)
        return b

    def init_saving(self):  #KEEP THIS PORTION OF THE CODE (COMMENTED SO THAT IT DOESNT ALWAYS SAVE)
        pass
        # write data to file:
        # self.write_data_to_file = WriteDataToFile(self.save_path,
        #                                           self.gv.data_queue, self.gv.t_queue,
        #                                           self.gv.experiment_queue,
        #                                           self.gv.n_data_created, self.lock)
        # # self.write_data_to_file.start()
        # self.write_data_to_file.at_exit_job()

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
        row=1; col=0; rowspan=1; colspan=1
        # Add to tab layout
        self.fft_layout.addWidget(self.fft_plot, row, col, rowspan, colspan)
        # Associate the plot to an FftGraph object
        self.fft_plot_obj = FftGraph(self.fft_plot, self.gv, self.pen_color)
        self.timer_fft.timeout.connect(self.fft_plot_obj.update_fft_plotting)

    def init_eeg_plot(self):
        """
        """
        for ch in range(self.gv.N_CH + 1):
            self.eeg_plot = pg.PlotWidget(background=(3, 3, 3))
            self.eeg_plot.plotItem.showGrid(x=True, y=True, alpha=0.2)
            # Use log scale to have a better visualization of the FFT data

            # Add the label only for the last channel as they all have the same
            self.eeg_plot.plotItem.setLabel(axis='left', units='v')
            if ch == 8:
                self.eeg_plot.plotItem.setLabel(axis='bottom', text='Time',
                                                units='s')                     # Todo : ALEXM : verifier l'uniter
                rowspan = 1
                queue = self.zero_data_queue # So that we don't see it
            else:

                self.eeg_plot.plotItem.hideAxis('bottom')
                rowspan = 3
                queue = self.gv.data_queue[ch]
            # Add the widget to the layout at the proper position
            row=ch*3+3; col=1; colspan=2

            self.eeg_layout.addWidget(self.eeg_plot, row, col, rowspan, colspan)
            # Update plotting
            self.eeg_plots.append(EegGraph(self.eeg_plot, queue, self.gv,
                                           self.pen_color[ch], ch, self.lock,
                                           self.last_classified_type))

            self.timers_eeg[ch].timeout.connect(self.eeg_plots[ch].update_eeg_plotting)

    def init_wave_plot(self):
        """
        """
        self.wave_plot = pg.PlotWidget(background=(3, 3, 3))
        self.wave_plot.plotItem.setLabel(axis='left', text='Power',
                                        units='None')
        self.wave_plot.plotItem.hideAxis('bottom')
        row=1; col=0; rowspan=1; colspan=1
        # Add to tab layout
        self.wave_layout.addWidget(self.wave_plot, row, col, rowspan, colspan)
        # Create the bar chart only for the first channel
        self.one_ch_deque = self.gv.data_queue[0]
        self.wave_plot_obj = WaveGraph(self.wave_plot, self.one_ch_deque)
        # self.timer_show_classif.timeout.connect(self.wave_plot_obj.update_wave_plotting)
        """
        mne_head = QLabel(self.main_window)
        mne_head.setPixmap(QtGui.QPixmap('./logo/mne_head.png'))
        row=2; col=0; rowspan=1; colspan=1
        self.wave_layout.addWidget(mne_head, row, col, rowspan, colspan)
        """

    def init_show_classif_plot(self):
        # --- Bar chart ---
        self.show_classif_plot = pg.PlotWidget(background=(3, 3, 3))
        self.show_classif_plot.plotItem.setLabel(axis='left', text='Power',
                                                 units='None')
        self.show_classif_plot.setYRange(0, 12)
        # Add to tab layout
        row=0; col=0; rowspan=1; colspan=1
        self.show_classif_layout.addWidget(self.show_classif_plot,
                                           row, col, rowspan, colspan)
        # --- Number of classification per type graph ---
        # Create the plot widget and its characteristics
        self.n_classif_plot = pg.PlotWidget(background=(3, 3, 3))
        self.n_classif_plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        self.n_classif_plot.plotItem.setLabel(axis='bottom',
                                              text='n classification time')
        self.n_classif_plot.plotItem.setLabel(axis='left',
                                              text='n classification')
        row=1; col=0; rowspan=1; colspan=1
        # Add to tab layout
        self.show_classif_layout.addWidget(self.n_classif_plot,
                                           row, col, rowspan, colspan)
        # Create the object to update the bar chart graph and the line graph
        self.live_classification = LiveClassification(self.gv,
                                                      self.show_classif_plot,
                                                      self.n_classif_plot,
                                                      self.last_classified_type,
                                                      self.gv.n_data_created)
        self.timer_classif.timeout.connect(
                self.live_classification.update_all)


class WaveGraph:
    def __init__(self, wave_plot, one_ch_deque):
        self.wave_plot = wave_plot
        self.one_ch_deque = one_ch_deque

        self.x = np.arange(10)
        self.y = np.sin(self.x)
        self.bg1 = pg.BarGraphItem(x=self.x, height=self.y, width=1, brush='b')
        self.wave_plot.addItem(self.bg1)

    def update_wave_plotting(self):
        # Remove All item from the graph
        self.wave_plot.clear()
        self.y = np.random.random(10)
        self.bg1 = pg.BarGraphItem(x=self.x, height=self.y, width=1, brush='b')
        self.wave_plot.addItem(self.bg1)


class EegGraph:
    """
    """
    def __init__(self, eeg_plot, one_ch_deque, gv, pen_color, ch, lock,
                 last_classified_type):
        self.eeg_plot = eeg_plot
        self.one_ch_deque = one_ch_deque
        self.gv = gv
        self.last_n_data_created = self.gv.n_data_created[0]
        self.ch = ch
        self.lock = lock
        self.last_classified_type = last_classified_type

        self.N_DATA = len(one_ch_deque)
        self.curve_eeg = self.eeg_plot.plot(self.gv.t_queue,
                                            deque(np.zeros(self.N_DATA),
                                            maxlen=self.N_DATA))
        self.curve_eeg.setPen(pen_color)
        # Show the position where events in experiments happen
        self.regions = []
        red = (255, 0, 0, 40)
        green = (0, 255, 0, 40)
        blue = (0, 0, 255, 40)
        yellow = (255, 255, 0, 40)
        purple = (146, 56, 219, 40)
        self.region_brush = [red, green, blue, yellow, purple]
        self.brush = self.region_brush[1]
        self.exp_queue_temp = self.gv.experiment_queue
        # Show classification live on the grap
        self.r_in_use = []
        self.r_waiting = []
        self.r_to_delete = []

        for line_no in range(20):
            self.r_waiting.append(line_no)
            self.regions.append([self.N_DATA, pg.LinearRegionItem([0, 0])])
            self.eeg_plot.addItem(self.regions[line_no][1], ignoreBounds=True)

    def update_eeg_plotting(self):
        if self.ch == 8:
            # WARNING: When I plot with the time, the quality of the signal degrade
            self.curve_eeg.setData(self.gv.t_queue, self.one_ch_deque)
            # Put the queue in a temp so that it's only changes once every cycle
            self.exp_queue_temp = self.gv.experiment_queue
            # self.last_classified_type[0] = 0
        else:
            self.curve_eeg.setData(self.one_ch_deque)
            # Add vertical lines where experiment events happen (then add box with text)
            # Do all these action in one line so that its not split with an other thread    TODO: ALEXM Use a lock instead (didn't seems to work)
            non_zero_type = np.array(self.exp_queue_temp)[np.nonzero(np.array(self.exp_queue_temp))[0]]
            non_zero_pos = np.nonzero(np.array(self.exp_queue_temp))[0]

            # Set the position of the regions delimiting events (when an
            # an experiment is playing
            if non_zero_type != []:
                for no, (pos, n_z_type) in enumerate(zip(non_zero_pos, non_zero_type)):
                    self.brush = self.region_brush[int(n_z_type)]
                    self.regions[no][1].setBrush(self.brush)
                    self.regions[no][1].setRegion([pos, pos+150])

            # --- Classification events ---
            if self.ch == 3:
                # Create region if event occure and add it to the list that update
                # Their position. And if there is enough region left
                if self.last_classified_type[0] and self.r_waiting:
                    spawn_region = self.r_waiting.pop()
                    # Select brush type based on event type
                    brush = self.region_brush[self.last_classified_type[0] - 6]
                    self.regions[spawn_region][1].setBrush(brush)
                    self.regions[spawn_region][1].setRegion([self.N_DATA-170,
                                                             self.N_DATA])
                    self.r_in_use.append(spawn_region)
                    self.last_classified_type[0] = 0
                # keep track of the number of data that was created between call
                # to this function so that the regions pos is updated accordingly
                delta_data = self.gv.n_data_created[0] - self.last_n_data_created
                self.last_n_data_created = self.gv.n_data_created[0]
                # Move regions that are in use at every itteration
                if self.r_in_use:
                    for r_no in self.r_in_use:
                        self.regions[r_no][0] -= delta_data
                        pos = self.regions[r_no][0]
                        self.regions[r_no][1].setRegion([pos-170, pos])
                        # Remove region out of view
                        if self.regions[r_no][0] < 0:
                            self.r_waiting.append(r_no)
                            self.regions[r_no][1].setRegion([self.N_DATA,
                                                             self.N_DATA])
                            self.regions[r_no][0] = self.N_DATA
                            self.r_to_delete.append(r_no)

                # Remove the regions that are out of the view
                if self.r_to_delete:
                    self.r_in_use = [x for x in self.r_in_use \
                                     if x not in self.r_to_delete]
                    self.r_to_delete = []

    def remove_ch_from_plotting(self):
        pass
        # This allows us to remove a ch from being plot
        # Je dois aussi arreter d'aller voir la channel sur le open bci:
        # Faire un timer par channel instead


class FftGraph:
    """
    """
    def __init__(self, freq_plot, gv, pen_color):
        self.gv = gv
        self.freq_plot = freq_plot
        self.pen_color = pen_color

        self.N_DATA = len(self.gv.data_queue[0])
        self.gv.N_CH = len(self.gv.data_queue)

        self.curve_freq = []
        for ch in range(self.gv.N_CH):
            self.curve_freq.append(freq_plot.plot(deque(np.zeros(self.N_DATA),
                                                        maxlen=self.N_DATA)))

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


class ChNumberAction:
    def __init__(self, timers_eeg, ch):
        self.timers_eeg = timers_eeg
        self.ch = ch

    @QtCore.pyqtSlot(bool)
    def stop_ch(self, checked):
        if checked:
            self.timers_eeg[self.ch].stop()
        else:
            self.timers_eeg[self.ch].start()


class ActionButton:
    def __init__(self, gv, layout, b_n, ch, pos):
        self.gv = gv
        self.b_n = b_n
        self.ch = ch
        # self.tab = tab
        self.layout = layout
        self.pos = pos
        self.style = ("""QLabel {background-color: rgba(0, 0, 0, 0); 
                         color: rgba(150, 150, 150, 220)}""")
        # Create timer
        self.timer_avg = QtCore.QTimer()
        self.timer_max = QtCore.QTimer()
        # Create labels
        self.avg_label = QtGui.QLabel()
        self.max_label = QtGui.QLabel()

        self.create_avg_button()
        self.create_max_button()

    def create_avg_button(self):
        self.avg_label.setStyleSheet(self.style)
        # Set position of the label
        row=self.pos; col=2; rowspan=1; colspan=1
        self.layout.addWidget(self.avg_label, row, col, rowspan, colspan)

    def update_avg(self):
        # Create the average label
        avg_val = ' '*70 + f'{np.round(np.average(self.gv.data_queue[self.ch]), 2)} Vrms'
        self.avg_label.setText(avg_val)

    def create_max_button(self):
        # Create the average label                                             # TODO: ALEXM Enlever la répétition
        self.max_label.setStyleSheet(self.style)
        # Set position of the label
        row=self.pos; col=2; rowspan=1; colspan=1
        self.layout.addWidget(self.max_label, row, col, rowspan, colspan)

    def update_max(self):
        max_val = ' ' *70 + f'{np.round(np.max(self.gv.data_queue[self.ch]), 2)} Vrms'
        self.max_label.setText(max_val)

    @QtCore.pyqtSlot(bool)                                                            # TODO: ALEXM remove this duplicate
    def show_avg(self, checked):
        if checked:
            # Update the average label
            self.timer_avg.timeout.connect(self.update_avg)
            self.timer_avg.start(400)
        else:
            self.avg_label.setText('')
            self.timer_avg.stop()

    @QtCore.pyqtSlot(bool)
    def show_max(self, checked):
        if checked:
            # Update the average label
            self.timer_max.timeout.connect(self.update_max)
            self.timer_max.start(400)
        else:
            self.max_label.setText('')
            self.timer_max.stop()


class LiveClassification:
    def __init__(self, gv, show_classif_plot, n_classif_plot,
                 last_classified_type, n_data_created):
        self.gv = gv
        self.last_classified_type = last_classified_type
        clf_path = 'machine_learning/linear_svm_fitted_model.pkl'
        self.clf = joblib.load(os.path.join(os.getcwd(), clf_path))
        self.n_tot_predict = 0
        self.last_classif = np.array([0 for _ in range(15)])
        self.i = 0
        # Classification
        self.show_classif_plot = show_classif_plot
        self.init_show_classif()
        # n classification plot
        N_DATA = 200
        self.N_CLASSIF_TYPE = 3
        self.pen_color = ['r', 'b', 'g']
        self.n_classif_plot = n_classif_plot
        self.n_classif_queue = [deque(np.zeros(N_DATA), maxlen=N_DATA) \
                                for _ in range(self.N_CLASSIF_TYPE)]
        self.curve_n_classif = []
        self.REFRACT_PERIOD_T = 0.7
        self.refract_period_init_t = 0
        self.is_refract_period = False
        for ch in range(self.N_CLASSIF_TYPE):
            self.curve_n_classif.append(n_classif_plot.plot(deque(np.zeros(N_DATA),
                                                            maxlen=N_DATA)))

    def init_show_classif(self):
        self.x = np.arange(9)
        self.y = np.array(np.zeros(9))
        self.bg1 = pg.BarGraphItem(x=self.x, height=self.y, width=1, brush='b')
        self.show_classif_plot.addItem(self.bg1)

    def update_all(self):
        self.classify_incoming_data()
        self.update_bar_chart_plotting()
        self.update_n_classif_plotting()

    def classify_incoming_data(self):
        data_queue = np.array(self.gv.data_queue[3])
        emg_signal = data_queue[-170:]
        # Evaluate the classificaiton type
        if emg_signal.any():  # if all not all zero array
            # Uniformize data to help for prediction
            emg_signal = uniformize_data(emg_signal, len(emg_signal))
            # Prediction
            class_type = self.clf.predict([emg_signal])[0]
        else:
            class_type = 0
        self.last_classif[self.i] = class_type

        # update refracting period to false if the refraction time is passed
        if self.is_refract_period:
            if time() - self.refract_period_init_t > self.REFRACT_PERIOD_T:
                self.is_refract_period = False
        else:
            self.y = np.bincount(self.last_classif, minlength=9)
        # Keep track of the classification type at each itt to live graph it
        for i, classif_type in enumerate([0, 6, 7]): 
            self.n_classif_queue[i].append(self.y[classif_type])
        # Select the event of a certain type if over a threshold of firering
        # Type CLOSE
        if self.y[6] >= 4:
            self.y = np.array(np.zeros(9))
            self.last_classified_type[0] = 6
            self.refract_period_init_t = time()
            self.is_refract_period = True
        # Type PINCH
        elif self.y[7] >= 4:
            self.y = np.array(np.zeros(9))
            self.last_classified_type[0] = 7
            self.refract_period_init_t = time()
            self.is_refract_period = True

        # Increase itt
        self.i += 1
        if self.i == 10:
            self.i = 0

    def update_bar_chart_plotting(self):
        # Remove All item from the graph
        self.show_classif_plot.clear()
        self.bg1 = pg.BarGraphItem(x=self.x, height=self.y, width=1, brush='b')
        self.show_classif_plot.addItem(self.bg1)
        
    def update_n_classif_plotting(self): 
        for classif_type in range(self.N_CLASSIF_TYPE):
            # Don't show the 0 values it's redondant                           # TODO: ALEXM Remove it in the dataqueue
            if classif_type:
                self.curve_n_classif[classif_type].setData(
                        self.n_classif_queue[classif_type])
                self.curve_n_classif[classif_type].setPen(self.pen_color[classif_type])
        



