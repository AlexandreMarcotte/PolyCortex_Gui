# -- General packages --
from collections import deque
import numpy as np
import pyqtgraph as pg
from functools import partial
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from collections import namedtuple

# -- My packages --
## generate signal
from generate_signal.from_openbci import stream_data_from_OpenBCI
from generate_signal.from_fake_data import CreateFakeData
from generate_signal.from_file import CreateDataFromFile

from .ch_number_action import ChNumberAction
from .action_button import ActionButton

from app.colors import *
from app.activation_b import btn
from tabs.region import Regions
from .eeg_graph import EegGraph


class EegPlotsCreator:
    def __init__(self, gv, layout, data_saver):
        self.gv = gv
        self.ts = self.gv.t_queue
        self.layout = layout
        self.timers = []
        # Contain all the button for all the ch w the specif actn they trigger
        self.actn_btns_func = []
        self.actn_btns = []
        # self.last_classified_type = last_classified_type
        self.stream_path = f'./experiment_csv/2exp_pinch_close_2018-08-29 19:44:54.567417.csv'
        self.plots = []
        self.eeg_graphes = []
        self.zero_q = deque(
            np.zeros(self.gv.DEQUE_LEN), maxlen=self.gv.DEQUE_LEN)

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
            eeg_graph = EegGraph(ch, q, self.gv, self.ts, curve, self.regions)
            self.eeg_graphes.append(eeg_graph)
            self.timers.append(QtCore.QTimer())
            self.timers[ch].timeout.connect(self.eeg_graphes[ch].update_graph)
            self.assign_n_to_ch(ch)
        self.assign_action_to_ch()

    def init_layouts(self):
        self.ch_layouts = []
        self.ch_group = []
        for ch in range(self.gv.N_CH):
            self.ch_layouts.append(QGridLayout())
            self.ch_group.append(QGroupBox(f'ch'))
            self.ch_group[ch].setLayout(self.ch_layouts[ch])

    def create_buttons(self):
        """Assign pushbutton for starting and stoping the stream"""
        btn('Start streaming', self.layout, (2, 1),
            func_conn=self.start_streaming, color=green_b)
        btn('Stop streaming', self.layout, (2, 2),
            func_conn=self.stop_streaming, color=red_b)

    def create_plot(self, ch:int):
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
        self.n_classif_regions_per_plot = 10
        self.regions = Regions(self.gv, self.n_classif_regions_per_plot)
        for i in range(self.n_classif_regions_per_plot):
            # The first value in the .list correspond to the position of the
            # region on the graph
            self.regions.list.append([self.gv.DEQUE_LEN,
                                      pg.LinearRegionItem([0, 0])])
            plot.addItem(self.regions.list[i][1], ignoreBounds=True)
        return plot

    def create_curve(self, plot, ch, q):
        """Create curves associated with the plots"""
        eeg_curve = plot.plot(self.ts, q)
        eeg_curve.setPen(pen_colors[ch])
        return eeg_curve

    def assign_n_to_ch(self, ch):
        if ch != self.gv.N_CH:
            ch_number_action = ChNumberAction(self.timers, ch)
            # +1 so the number str start at 1
            btn(name=str(ch + 1), layout=self.layout, pos=(ch * 4 + 4, 0),
                func_conn=ch_number_action.stop_ch,
                color=button_colors[ch], toggle=True, max_width=18)

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
        for i, tm in enumerate(self.timers):
            self.timers[i].start()

    def stop_timers(self):
        for i, tm in enumerate(self.timers):
            self.timers[i].stop()

    def assign_action_to_ch(self):
        pos = 4
        m_w = 17
        tot_b = 0
        N_BTN_PER_CH = 4
        for ch in range(self.gv.N_CH):
            for b_n in range(N_BTN_PER_CH):
                # Create an action object and add it to the list of all actions
                # in the tab
                actn_btn = ActionButton(self.gv, self.layout, b_n, ch, pos)
                self.actn_btns.append(actn_btn)
                # Average
                if b_n % N_BTN_PER_CH == 0:                               # TODO: ALEXM replace this if else by something similar to a switch case
                    btn('A', self.layout, (pos, 3),
                        func_conn=self.actn_btns[tot_b].show_avg,
                        toggle=True, tip='Show average value of queue',
                        max_width=m_w, color=grey)
                # Max
                elif b_n % N_BTN_PER_CH == 1:
                    # Create a max action
                    btn('M', self.layout, (pos, 3),
                        func_conn=self.actn_btns[tot_b].show_max,
                        toggle=True, tip='Show max value of queue',
                        max_width=m_w, color=grey)
                # Detection
                elif b_n % N_BTN_PER_CH == 2:
                    pos-=2 #  Return at the upper position
                    btn('D', self.layout, (pos, 4),
                        toggle=True, tip='Show detected class patern',
                        max_width=m_w, color=grey)
                # Other function
                elif b_n % N_BTN_PER_CH == 3:
                    btn('O', self.layout, (pos, 4), toggle=True,
                        tip='Show other action', max_width=m_w, color=grey)
                pos += 1
                # Change the total number of buttons
                tot_b += 1
            # Add a vertical line to delineate the action for each channel
            # line = QFrame(self.main_window)
            # line.setGeometry(QtCore.QRect())
            # line.setFrameShape(QFrame.HLine)
            # line.setFrameShadow(QFrame.Sunken)
            # self.layout.addWidget(line, pos, 3, 1, 2)
            pos += 2