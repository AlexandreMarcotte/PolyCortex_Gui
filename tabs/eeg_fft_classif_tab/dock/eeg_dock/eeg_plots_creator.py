# -- General packages --
from collections import deque
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
import re
from functools import partial
# -- My packages --
## generate signal
from generate_signal.from_openbci import SampleDataFromOPENBCI
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
from app.pyqt_frequently_used import create_txt_label, create_combo_box


class EegPlotsCreator:
    def __init__(self, gv, layout):
        self.gv = gv
        self.layout = layout

        self.btns = []
        self.ts = self.gv.t_queue
        self.timers = []
        self.plots = []
        self.eeg_graphes = []
        self.zero_q = deque(
            np.zeros(self.gv.DEQUE_LEN), maxlen=self.gv.DEQUE_LEN)

        # Stop/Start
        start_stop_layout = self.add_sub_layout(self.layout, pos=(0, 0))

        self.create_buttons(start_stop_layout)
        # Plot parameter
        self.create_param_combo_box(start_stop_layout)

        self.create_all_eeg_plot()

    def set_saver(self, data_saver):
        self.data_saver = data_saver

    def create_param_combo_box(self, start_stop_l):
        self.create_settings_combo_box(
            'Vertical scale', start_stop_l, (1, 0),
            ['Auto', '10 uv', '100 uv', '1000 uv', '10000 uv', '100000 uv'],
            editable=True, connect_func=self.scale_y_axis)
        self.create_settings_combo_box(
            'Horizontal scale', start_stop_l, (1, 2), ['5 s', '7 s', '10 s'])
        self.create_settings_combo_box(
            'Number of columns', start_stop_l, (1, 4), ['1', '2'])

    def create_settings_combo_box(self, title, layout, pos, settings_list,
                                      editable=False, connect_func=None):
        l = create_txt_label(title)
        layout.addWidget(l, *pos)
        cb = create_combo_box(settings_list, connect_func=connect_func,
                              editable=editable)
        layout.addWidget(cb, pos[0], pos[1]+1)

    def scale_y_axis(self, txt):
        try:
            if txt == 'Auto':
                for plot in self.plots:
                    plot.enableAutoRange()
            else:
                r = int(re.search(r'\d+', txt).group())
                for plot in self.plots:
                    plot.setYRange(-r, r)
        except AttributeError as e:
            print("Come on bro, this  value doesn't make sens")

    def create_all_eeg_plot(self):
        """
        """
        num_col = 1
        ch = 0
        for ch in range(self.gv.N_CH):
            if num_col == 1:
               col_factor = 8
            elif num_col == 2:
                col_factor = 4
            else: col_factor = 8

            self.ch_layout = self.add_sub_layout(self.layout,
                                                 (ch%col_factor+1, ch//col_factor))
            self.add_ch_layout(ch)
            # Put only a plot on the time channel
        self.add_ch_layout(ch=self.gv.N_CH, time_ch=True, plot_pos=(5, 1, 1, 6))

    def add_ch_layout(self, ch, time_ch=False, plot_pos=(0, 1, 5, 6)):
        plot, q, rowspan = self.create_plot(ch)
        self.plots.append(plot)
        self.ch_layout.addWidget(plot, *plot_pos)
        curve = self.create_curve(plot, ch, q)
        eeg_graph = EegGraph(ch, q, self.gv, self.ts, curve, self.regions)
        self.eeg_graphes.append(eeg_graph)
        self.timers.append(QtCore.QTimer())
        self.timers[ch].timeout.connect(self.eeg_graphes[ch].update_graph)
        if not time_ch:
            self.assign_n_to_ch(ch)
            self.assign_action_to_ch(ch)

    def add_sub_layout(self, parent_layout, pos, shape=(1, 1)):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        gr = QGroupBox(f'')
        gr.setLayout(layout)
        parent_layout.addWidget(gr, *pos, *shape)
        return layout

    def create_buttons(self, layout):
        """Assign pushbutton for starting"""
        btn('Start streaming', layout, (0, 0), size=(1, 6), toggle=True,
            func_conn=self.start_timers, color=blue_b, txt_color=white)

    def create_plot(self, ch):
        """Create a plot for all eeg signals and the last to keep track of time"""
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.showGrid(x=True, y=True, alpha=0.2)
        plot.plotItem.setLabel(axis='left', units='v')
        plot.setYRange(-3000, 3000)
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
        self.btn = btn(name=str(ch + 1), layout=self.ch_layout, pos=(0, 0),
                       func_conn=ch_number_action.stop_ch,
                       color=button_colors[ch], toggle=True, max_width=18)
        self.btns.append(self.btn)

    def init_streaming_source(self):
        """      """
        if self.gv.stream_origin == 'Stream from OpenBCI':
            stream_source = SampleDataFromOPENBCI(self.gv)
        elif self.gv.stream_origin == 'Stream from synthetic data':
            # Create fake data for test case
            stream_source = CreateSyntheticData(
                self.gv, callback=self.gv.collect_data,
                read_freq=self.gv.DEQUE_LEN)

        elif self.gv.stream_origin == 'Stream from file':
            stream_source = FileReader(
                self.gv, self.gv.stream_path, self.gv.collect_data,
                read_freq=250)
        else:
            raise('No streaming source selected')

        return stream_source

    @QtCore.pyqtSlot(bool)
    def start_timers(self, checked):
        stream_source = self.init_streaming_source()
        if checked:
            self.freq_counter = FrequencyCounter(self.gv)
            stream_source.start()
            for i, tm in enumerate(self.timers):
                self.timers[i].start(0)
            self.start_freq_counter_timer()
        else:
            for i, tm in enumerate(self.timers):
                self.timers[i].stop()
            # self.stream_source.join()

    def start_freq_counter_timer(self):
        self.freq_counter_timer = QtCore.QTimer()
        self.freq_counter_timer.timeout.connect(self.freq_counter.update)
        self.freq_counter_timer.start(50)

    def assign_action_to_ch(self, ch):
        m_w = 17
        # Average
        actn_btn = ActionButton(self.ch_layout, 0, self.gv, ch)
        btn('A', self.ch_layout, (0, 8), action=actn_btn,
            toggle=True, tip='Show average value of queue',
            max_width=m_w, color=dark_blue_tab)
        # Max
        actn_btn = ActionButton(self.ch_layout, 1, self.gv, ch)
        btn('M', self.ch_layout, (1, 8), action=actn_btn,
            toggle=True, tip='Show max value of queue',
            max_width=m_w, color=dark_blue_tab)
        # Detection
        btn('D', self.ch_layout, (2, 8),
            toggle=True, tip='Show detected class patern',
            max_width=m_w, color=dark_blue_tab)

        self.create_color_button(ch)

    def create_color_button(self, ch):
        """Create color button to change the color of the line"""
        color_btn = pg.ColorButton(close_fit=True)
        color_btn.setMaximumWidth(14)
        color_btn.setToolTip('Click to change the color of the line')
        color_btn.sigColorChanged.connect(partial(self.change_line_color, ch))
        self.ch_layout.addWidget(color_btn, 3, 8)

    def change_line_color(self, ch, color_btn):
        color = color_btn.color()
        self.eeg_graphes[ch].curve.setPen(color)
        self.gv.curve_freq[ch].setPen(color)
        self.btns[ch].set_color(color)
