from collections import deque
import numpy as np
import pyqtgraph as pg
from functools import partial
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot

# My packages
## generate signal
from generate_signal.from_openbci import stream_data_from_OpenBCI
from generate_signal.from_fake_data import CreateFakeData
from generate_signal.from_file import CreateDataFromFile

from .ch_number_action import ChNumberAction
from .action_button import ActionButton

from app.colors import *
from app.activation_b import activation_b
from tabs.region import Regions
from .eeg_graph import EegGraph


class EegPlotsCreator:
    def __init__(self, gv, layout, data_saver):
        self.gv = gv
        self.ts = self.gv.t_queue
        self.layout = layout
        self.timers = []
        ## Action
        # Start the position at two because the buttons start on the second row
        self.tot_b_num = 0
        self.pos = 4
        self.N_BUTTONS_PER_CH = 4
        # Contain all the button for all the ch w the specif actn they trigger
        self.actn_btns_func = []
        self.actn_btns = []
        # self.last_classified_type = last_classified_type
        self.stream_path = f'./experiment_csv/2exp_pinch_close_2018-08-29 19:44:54.567417.csv'
        self.plots = []
        self.eeg_graphes = []
        self.zero_q = deque(
            np.zeros(self.gv.DEQUE_LEN), maxlen=self.gv.DEQUE_LEN)
        # Regions
        self.n_classif_regions_per_plot = 2

        self.create_all_eeg_plot()
        self.create_buttons()

        # Saving
        self.data_saver = data_saver
        self.data_saver.save_data_to_file()

    def create_all_eeg_plot(self):
        """
        """
        for ch in range(self.gv.N_CH + 1):
            plot, q, rowspan = self.create_plot(ch)
            self.layout.addWidget(plot, ch * 4 + 3, 1, rowspan, 2)
            curve = self.create_curve(plot, ch, q)
            eeg_graph = EegGraph(ch, q, self.ts, curve, self.regions)
            self.eeg_graphes.append(eeg_graph)
            self.timers.append(QtCore.QTimer())
            self.timers[ch].timeout.connect(self.eeg_graphes[ch].update_graph)
            self.assign_n_to_ch(ch)
            self.assign_action_to_ch(ch)

    def create_buttons(self):
        """Assign pushbutton for starting and stoping the stream"""
        activation_b(self.layout, 'Start streaming', self.start_streaming,
                     (2, 1), green_b)
        activation_b(self.layout, 'Stop streaming', self.stop_streaming,
                     (2, 2), red_b)

    def create_plot(self, ch):
        """Create a plot for all eeg signals and the last to keep track of time"""
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.showGrid(x=True, y=True, alpha=0.2)
        plot.plotItem.setLabel(axis='left', units='v')
        # Create the last plot only to keep track of the time (with zeros as q)
        if ch == self.gv.N_CH:
            # Add the label only for the last channel as they all have the same
            plot.plotItem.setLabel(axis='bottom', text='Time', units='s')  # Todo : ALEXM : verifier l'uniter
            rowspan = 1
            q = self.zero_q  # So that we don't see it
        else:
            plot.plotItem.hideAxis('bottom')
            rowspan = 4
            q = self.gv.data_queue[ch]

        self.add_classif_regions_to(plot)

        return plot, q, rowspan

    def add_classif_regions_to(self, plot):
        """Create colored region (10) and placed them all at the beginning
           of each plot (will be used to indicated classification of a
           region of the signal or event occured in experiments"""
        self.regions = Regions(self.gv, self.n_classif_regions_per_plot)
        for i in range(self.n_classif_regions_per_plot):
            self.regions.list.append(pg.LinearRegionItem([0, 0]))
            plot.addItem(self.regions.list[i], ignoreBounds=True)
        return plot

    def create_curve(self, plot, ch, q):
        """Create curves associated with the plots"""
        eeg_curve = plot.plot(self.ts, q)
        eeg_curve.setPen(pen_colors[ch])
        return eeg_curve

    def assign_n_to_ch(self, ch):
        if ch != self.gv.N_CH:
            # +1 so the number str start at 1
            b_on_off_ch = QtGui.QPushButton(str(ch + 1))
            b_on_off_ch.setCheckable(True)
            b_on_off_ch.setToolTip('Stop current channel')
            style = ('QPushButton {background-color'
                     + ': {color}; '.format(color=button_colors[ch])
                     + 'min-width: 14px}')
            b_on_off_ch.setStyleSheet(style)
            ch_number_action = ChNumberAction(self.timers, ch)
            b_on_off_ch.toggled.connect(partial(ch_number_action.stop_ch))
            # Set position and size of the button values
            self.layout.addWidget(b_on_off_ch, ch * 4 + 4, 0)

    @pyqtSlot()
    def start_streaming(self):
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

        self.start_timers()
        # SAVE the data received to file
        self.save_path = self.data_saver.save_path_line_edit.text()
        self.data_saver.init_saving()

    @pyqtSlot()
    def stop_streaming(self):
        if self.gv.stream_origin[0] == 'Stream from OpenBCI':
            self.board.stop()
        self.stop_timers()
        # Stop saving process
        # self.write_data_to_file.join()

    def start_timers(self):
        for tm in self.timers:
            tm.start()

    def stop_timers(self):
        for tm in self.timers:
            tm.stop()

    def assign_action_to_ch(self, ch):
        if ch != self.gv.N_CH:
            for b_n in range(self.N_BUTTONS_PER_CH):
                # Create an action object and add it to the list of all actions
                # in the tab
                action_button = ActionButton(self.gv, self.layout,
                                             b_n, ch, self.pos)
                self.actn_btns.append(action_button)
                # Average
                if b_n % self.N_BUTTONS_PER_CH == 0:
                    col = 3
                    b = self.create_actn_btn(
                        self.tot_b_num, 'A', tip='Show average value of queue',
                        func_conn=self.actn_btns[self.tot_b_num].show_avg)
                # Max
                elif b_n % self.N_BUTTONS_PER_CH == 1:
                    col = 3
                    # Create a max action
                    b = self.create_actn_btn(
                        self.tot_b_num, 'M', tip='Show max value of queue',
                        func_conn=self.actn_btns[self.tot_b_num].show_max)

                # Detection
                elif b_n % self.N_BUTTONS_PER_CH == 2:
                    self.pos -= 2;
                    col = 4
                    b = self.create_actn_btn(
                        self.tot_b_num, 'D', tip='Show detected class patern')
                # Other function
                elif b_n % self.N_BUTTONS_PER_CH == 3:
                    col = 4
                    b = self.create_actn_btn(self.tot_b_num, 'O', 'Show other action')
                # Set self.position and size of the button values
                self.layout.addWidget(b, self.pos, col, 1, 1)
                self.pos += 1
                # Change the total number of buttons
                self.tot_b_num += 1
            # Add a vertical line to delineate the action for each channel
            # line = QFrame(self.main_window)
            # line.setGeometry(QtCore.QRect())
            # line.setFrameShape(QFrame.HLine)
            # line.setFrameShadow(QFrame.Sunken)
            # self.layout.addWidget(line, self.pos, 3, 1, 2)
            self.pos += 2

    def create_actn_btn(self, tot_b_num, actn_letter, actn_func=None,
                        tip='', checkable=True, func_conn=None):
        b = QtGui.QPushButton(actn_letter)
        b.setToolTip(tip)
        b.setCheckable(checkable)
        if func_conn:
            b.toggled.connect(partial(func_conn))
        return b