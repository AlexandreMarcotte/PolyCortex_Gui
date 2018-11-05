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
import time
import datetime
import atexit
import os
from collections import namedtuple
from time import time
# Classification
from data_processing_pipeline.uniformize_data import uniformize_data

# -- My packages --
## generate signal
from generate_signal.from_openbci import stream_data_from_OpenBCI
from generate_signal.from_fake_data import CreateFakeData
from generate_signal.from_file import CreateDataFromFile
# from save_to_file import WriteDataToFile
## Graphes
from .eeg_graph import EegPlotsCreator
from .wave_graph import WaveGraph
from .fft_graph import FftGraph
from .classification_graph import ClassifGraph
from .action_button import ActionButton
from .ch_number_action import ChNumberAction


class EegFftClassifTab:
    def __init__(self, main_window, tab_w, gv):
        super().__init__()
        self.main_window = main_window
        self.tab_w = tab_w
        self.gv = gv

        self.pen_colors = ['r', 'y', 'g', 'c', 'b', 'm',
                          (100, 100, 100), 'w', 'k']
        self.button_color = ['red', 'yellow', 'green', 'cyan',
                             'blue', 'magenta', 'grey', 'white']
        self.N_BUTTON_PER_CH = 4
        self.Pos = namedtuple('position', ['row', 'col', 'rowspan', 'colspan'])
        # Contain all the button for all the channels with the specif action
        # they trigger
        self.actn_btns_func = []

        # self.gv.n_data_created = n_data_created
        self.gv.N_CH = len(self.gv.data_queue)

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
        self.eeg_plot_creator = EegPlotsCreator(
            self.gv, self.eeg_layout, self.timers_eeg, self.pen_colors)
        # - FFT
        self.fft_graph = FftGraph(
            self.main_window, self.fft_layout,self.timer_fft, self.gv,
            self.pen_colors)
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



    def wave_plot_on_off_button(self):
        b = QPushButton('Show wave signal', self.main_window)
        b.setStyleSheet("background-color: rgba(0, 0, 80, 0.4)")
        self.wave_layout.addWidget(b, 0, 0, 1, 1)

    def add_banner(self):
        # Polycortex
        polycortex_banner = QLabel(self.main_window)
        polycortex_banner.setPixmap(QtGui.QPixmap('./logo/polycortex_banner.png'))
        self.banner_layout.addWidget(polycortex_banner, 0, 0, 1, 1)
        # OpenBci
        open_bci_banner = QLabel(self.main_window)
        open_bci_banner.setPixmap(QtGui.QPixmap('./logo/openbci_banner.png'))
        self.banner_layout.addWidget(open_bci_banner, 0, 1, 1, 1)

    def add_choose_streaming_file_b(self):
        # Create button to open date file
        self.choose_file = QtGui.QPushButton('Choose streaming file')
        self.choose_file.setStyleSheet("background-color: rgba(0, 0, 100, 0.5)")
        self.choose_file.clicked.connect(partial(self.choose_streaming_file))
        self.stream_layout.addWidget(self.choose_file, 0, 1, 1, 1)

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
        self.eeg_layout.addWidget(b_start, 2, 1, 1, 1)

    @pyqtSlot()
    def start_streaming_data(self):
        # -----Start streaming data from OPENBCI board ------
        if self.gv.stream_origin[0] == 'Stream from OpenBCI':
            self.board = stream_data_from_OpenBCI(self.gv)
        elif self.gv.stream_origin[0] == 'Stream from fake data':
            # Create fake data for test case
            create_data = CreateFakeData(self.gv)
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
        self.eeg_layout.addWidget(b_stop, 2, 2, 1, 1)

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
        self.saving_layout.addWidget(self.save_path_line_edit, 0, 0, 1, 2)
        # Create button to open date file
        open_file = QtGui.QPushButton('Choose saving directory')
        open_file.clicked.connect(partial(self.save_file_dialog))
        self.saving_layout.addWidget(open_file, 1, 0, 1, 1)
        # Button to save all the current data that was generated
        self.save_cur_data_b = QtGui.QPushButton('Save data Now')
        self.saving_layout.addWidget(self.save_cur_data_b, 1, 1, 1, 1)

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


    def init_saving(self):  #KEEP THIS PORTION OF THE CODE (COMMENTED SO THAT IT DOESNT ALWAYS SAVE)
        pass
        # write data to file:
        # self.write_data_to_file = WriteDataToFile(self.save_path,
        #                                           self.gv.data_queue, self.gv.t_queue,
        #                                           self.gv.experiment_queue,
        #                                           self.gv.n_data_created, self.lock)
        # # self.write_data_to_file.start()
        # self.write_data_to_file.at_exit_job()
    
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
            self.eeg_layout.addWidget(b_on_off_ch, ch*4+4, 0, 1, 1)

    def assign_action_to_ch(self):
        pos = 4  # Start the position at two because the buttons start on the second row
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
            self.line = QFrame(self.main_window)
            self.line.setGeometry(QtCore.QRect())
            self.line.setFrameShape(QFrame.HLine)
            # self.line.setFrameShadow(QFrame.Sunken)
            self.eeg_layout.addWidget(self.line, pos, 3, 1, 2)
            pos += 2
    
    def create_actn_btn(self, tot_b_num, actn_letter, actn_func=None,
                        tip='', checkable=True):
        b = QtGui.QPushButton(actn_letter)
        b.setToolTip(tip)
        b.setCheckable(checkable)
        return b

    def init_wave_plot(self):
        """
        """
        self.wave_plot = pg.PlotWidget(background=(3, 3, 3))
        self.wave_plot.plotItem.setLabel(axis='left', text='Power',
                                        units='None')
        self.wave_plot.plotItem.hideAxis('bottom')
        # Add to tab layout
        self.wave_layout.addWidget(self.wave_plot, 1, 0, 1, 1)
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
        self.show_classif_layout.addWidget(self.show_classif_plot, 0, 0, 1, 1)
        # --- Number of classification per type graph ---
        # Create the plot widget and its characteristics
        self.n_classif_plot = pg.PlotWidget(background=(3, 3, 3))
        self.n_classif_plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        self.n_classif_plot.plotItem.setLabel(axis='bottom',
                                              text='n classification time')
        self.n_classif_plot.plotItem.setLabel(axis='left',
                                              text='n classification')
        # Add to tab layout
        self.show_classif_layout.addWidget(self.n_classif_plot, 1, 0, 1, 1)
        # Create the object to update the bar chart graph and the line graph
        # self.classification_graph = LiveClassification(
        #     self.gv, self.show_classif_plot, self.n_classif_plot,
        #     self.last_classified_type, self.gv.n_data_created)
        #
        # self.timer_classif.timeout.connect(
        #         self.classification_graph.update_all)