# -- General packages --
from collections import deque
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
# -- My packages --
## generate signal
from generate_signal.from_openbci import stream_data_from_OpenBCI
from generate_signal.from_synthetic_data import CreateSyntheticData
from generate_signal.from_file import FileReader
from generate_signal.from_muse import StreamFromMuse

from .ch_number_action import ChNumberAction
from .action_button import ActionButton

from app.colors import *
from app.activation_b import btn
from tabs.region import Regions
from .eeg_graph import EegGraph

from data_processing_pipeline.frequency_counter import FrequencyCounter


class EegPlotsCreator:
    def __init__(self, gv, layout, data_saver):
        self.gv = gv
        self.ts = self.gv.t_queue
        self.layout = layout
        self.timers = []
        self.stream_path = f'experiment_csv/2exp_pinch_close_2018-08-29 18:55:22.627296.csv'
        self.plots = []
        self.eeg_graphes = []
        self.zero_q = deque(
            np.zeros(self.gv.DEQUE_LEN), maxlen=self.gv.DEQUE_LEN)

        # Stop/Start
        start_stop_layout = self.add_sub_layout(self.layout, 0)
        self.create_buttons(start_stop_layout)
        # Plot parameter
        self.create_param(start_stop_layout)

        self.create_all_eeg_plot()
        # Saving
        self.data_saver = data_saver
        self.data_saver.save_data_to_file()

    def create_param(self, start_stop_layout):
        vert_scale_txt = QLabel('    Vert scale: ')
        start_stop_layout.addWidget(vert_scale_txt, 1, 0)
        vert_scale = QComboBox()
        vert_scale.addItem('Auto')
        vert_scale.addItem('10 uv')
        vert_scale.addItem('100 uv')
        vert_scale.addItem('1000 uv')
        start_stop_layout.addWidget(vert_scale, 1, 1)

        horiz_scale = QLabel('    Horiz scale: ')
        start_stop_layout.addWidget(horiz_scale, 1, 2)
        horiz_scale = QComboBox()
        horiz_scale.addItem('5s')
        horiz_scale.addItem('7s')
        horiz_scale.addItem('10s')
        start_stop_layout.addWidget(horiz_scale, 1, 3)


    def create_all_eeg_plot(self):
        """
        """
        ch = 0
        for ch in range(self.gv.N_CH):
            self.ch_layout = self.add_sub_layout(self.layout, ch + 1)
            self.add_ch_layout(ch)
            # Put only a plot on the time channel
        self.add_ch_layout(ch=self.gv.N_CH, time_ch=True, plot_pos=(5, 1, 1, 6))

    def add_ch_layout(self, ch, time_ch=False, plot_pos=(0, 1, 5, 6)):
        plot, q, rowspan = self.create_plot(ch)
        self.ch_layout.addWidget(plot, *plot_pos)
        curve = self.create_curve(plot, ch, q)
        eeg_graph = EegGraph(ch, q, self.gv, self.ts, curve, self.regions)
        self.eeg_graphes.append(eeg_graph)
        self.timers.append(QtCore.QTimer())
        self.timers[ch].timeout.connect(self.eeg_graphes[ch].update_graph)
        if not time_ch:
            self.assign_n_to_ch(ch)
            self.assign_action_to_ch(ch)

    def add_sub_layout(self, parent_layout, pos):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        gr = QGroupBox(f'')
        gr.setLayout(layout)
        parent_layout.addWidget(gr, pos, 0)
        return layout

    def create_buttons(self, layout):
        """Assign pushbutton for starting and stoping the stream"""
        btn('Start streaming', layout, (0, 0), size=(1, 2),
            func_conn=self.start_streaming, color=green_b)
        btn('Stop streaming', layout, (0, 2), size=(1, 2),
            func_conn=self.stop_streaming, color=red_b)

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
        self.n_classif_regions_per_plot = 2
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
        ch_number_action = ChNumberAction(self.timers, ch)
        # +1 so the number str start at 1
        btn(name=str(ch + 1), layout=self.ch_layout, pos=(0, 0),
            func_conn=ch_number_action.stop_ch,
            color=button_colors[ch], toggle=True, max_width=18)

    @pyqtSlot()
    def start_streaming(self):
        """      """
        if self.gv.stream_origin == 'Stream from OpenBCI':
            self.board = stream_data_from_OpenBCI(self.gv)
        elif self.gv.stream_origin == 'Stream from synthetic data':
            # Create fake data for test case
            create_data = CreateSyntheticData(self.gv,
                                              callback=self.gv.collect_data,
                                              read_freq=self.gv.DEQUE_LEN)
            create_data.start()

        elif self.gv.stream_origin == 'Stream from file':
            file_reader = FileReader(self.gv, self.stream_path, self.gv.collect_data,
                                     read_freq=250)
            file_reader.start()

        elif self.gv.stream_origin == 'Stream from Muse':
            create_data = StreamFromMuse(self.gv)
            create_data.start()

        self.freq_counter = FrequencyCounter(self.gv)
        self.start_timers()
        # SAVE the data received to file
        self.save_path = self.data_saver.save_path_line_edit.text()
        # self.data_saver.init_saving()

    @pyqtSlot()
    def stop_streaming(self):
        if self.gv.stream_origin == 'Stream from OpenBCI':
            self.board.stop()
        self.stop_timers()

    def start_timers(self):
        for i, tm in enumerate(self.timers):
            self.timers[i].start()
        self.start_freq_counter_timer()

    def start_freq_counter_timer(self):
        self.freq_counter_timer = QtCore.QTimer()
        self.freq_counter_timer.timeout.connect(self.freq_counter.update)
        self.freq_counter_timer.start(50)

    def stop_timers(self):
        for i, tm in enumerate(self.timers):
            self.timers[i].stop()

    def assign_action_to_ch(self, ch):
        m_w = 17
        # Average
        actn_btn = ActionButton(self.ch_layout, 0, self.gv, ch)
        btn('A', self.ch_layout, (0, 8), action=actn_btn,
            toggle=True, tip='Show average value of queue',
            max_width=m_w, color=light_grey)
        # Max
        actn_btn = ActionButton(self.ch_layout, 1, self.gv, ch)
        btn('M', self.ch_layout, (1, 8), action=actn_btn,
            toggle=True, tip='Show max value of queue',
            max_width=m_w, color=light_grey)
        # Detection
        btn('D', self.ch_layout, (2, 8),
            toggle=True, tip='Show detected class patern',
            max_width=m_w, color=light_grey)
        # Other function
        btn('O', self.ch_layout, (3, 8), toggle=True,
            tip='Show other action', max_width=m_w, color=light_grey)

