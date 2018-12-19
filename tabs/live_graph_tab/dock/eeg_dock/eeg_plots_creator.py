# -- General Packages --
from collections import deque
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import re
from functools import partial
from pyqtgraph.dockarea import *
# -- My Packages --
# Generate signal
from generate_signal.from_openbci import SampleDataFromOPENBCI
from generate_signal.from_synthetic_data import CreateSyntheticData
from generate_signal.from_file import FileReader
# from generate_signal.from_muse import StreamFromMuse

from .ch_number_action import ChNumberAction
from .action_button import ActionButton

from app.colors import *
from app.activation_b import btn
from tabs.region import Regions
from .eeg_graph import EegGraph

from data_processing_pipeline.frequency_counter import FrequencyCounter
from app.pyqt_frequently_used import (
        create_param_combobox, create_splitter, create_gr)
from save.data_saver import DataSaver
from tabs.live_graph_tab.dock.banner_dock.banner import Banner

from tabs.live_graph_tab.dock.Inner_dock import InnerDock


class EegPlotsCreator:
    def __init__(self, gv, layout):
        # General Layout
        self.gv = gv
        self.layout = layout
        self.dock_area = DockArea()
        self.layout.addWidget(self.dock_area, 1, 0, 1, 8)

        # Variables
        self.btns = []
        self.ts = self.gv.t_queue
        self.timers = []
        self.plots = []
        self.eeg_graphes = []
        self.zero_q = deque(
                np.zeros(self.gv.DEQUE_LEN), maxlen=self.gv.DEQUE_LEN)
        self.GR_PER_COL = 1
        # Settings
        self.create_settings_dock()
        # Saving
        self.create_saving_dock()
        # Banner
        self.create_banner_dock()
        # EEG
        self.grps = self.create_all_eeg_plot()
        self.eeg_dock = self.create_eeg_dock(self.grps)

    def create_banner_dock(self):
        banner_d = InnerDock(
                self.layout, 'Banner', b_pos=(0, 2), b_checked=False,
                toggle_button=True, size=(1, 1))
        Banner(banner_d.layout)
        self.dock_area.addDock(banner_d.dock)
        banner_d.dock.hide()

    def create_saving_dock(self):
        saving_d = InnerDock(
                self.layout, 'Saving', b_pos=(0, 1), toggle_button=True,
                size=(1, 1))
        DataSaver(self.gv.main_window, self.gv, saving_d.layout, size=(1,1))
        self.dock_area.addDock(saving_d.dock)

    def create_settings_dock(self):
        settings_d = InnerDock(
                self.layout, 'Settings', toggle_button=True, size=(1, 1))
        # Stop/Start button
        self.create_buttons(settings_d.layout)
        # Plot parameter
        self.create_all_combobox(settings_d.layout)
        self.dock_area.addDock(settings_d.dock)

    def create_eeg_dock(self, grps):
        eeg_d = InnerDock(self.layout, 'Part EEG')
        splitters = self.create_splitter(grps)
        s_factor = len(splitters)//self.GR_PER_COL
        for no, s in enumerate(splitters):
            eeg_d.layout.addWidget(
                    s, no%s_factor, no//s_factor)
        self.dock_area.addDock(eeg_d.dock)
        return eeg_d

    @QtCore.pyqtSlot(bool)
    def open_dock(self, dock, checked):
        if checked:
            dock.show()
        else:
            dock.hide()

    def set_saver(self, data_saver):
        self.data_saver = data_saver

    def create_buttons(self, layout):
        """Assign pushbutton for starting"""
        btn('Start', layout, (0, 0), toggle=True, max_width=100,
            func_conn=self.start_timers, color=dark_blue_tab,
            txt_color=white)

    def create_all_combobox(self, start_stop_l):
        create_param_combobox(
                start_stop_l, 'Vertical scale', (0, 1),
                ['Auto', '10 uv', '100 uv', '1000 uv', '10000 uv', '100000 uv'],
                conn_func=self.scale_y_axis)
        create_param_combobox(
                start_stop_l, 'Horizontal scale', (0, 2), ['5s', '7s', '10s'],
                editable=False)
        create_param_combobox(
                start_stop_l, 'Nb of columns', (0, 3), ['1', '2', '4'],
                editable=False, conn_func=self.change_num_plot_per_row)

    def change_num_plot_per_row(self, plot_per_row):
        self.eeg_dock.dock.close()
        self.GR_PER_COL = int(plot_per_row)
        self.eeg_dock = self.create_eeg_dock(self.grps)

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
        grps = []
        for ch in range(self.gv.N_CH):
            self.gr, self.ch_layout = create_gr()
            grps.append(self.gr)
            self.add_ch_layout(ch)
            # Put only a plot on the time channel
        self.add_ch_layout(ch=self.gv.N_CH, time_ch=True,
                           plot_pos=(5, 1, 1, 6))
        return grps

    def add_ch_layout(self, ch, time_ch=False, plot_pos=(0, 1, 5, 6)):      # TODO: ALEXM: change the name of this function
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

    def create_splitter(self, grps):
        splitters = []
        for i in range(0, len(grps), 2):
            splitter = create_splitter(
                    grps[i], grps[i+1], direction=Qt.Vertical)
            splitters.append(splitter)
        return splitters

    def create_plot(self, ch):
        """Create a plot for all eeg signals and the last to keep track of time"""
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.showGrid(x=True, y=True, alpha=0.2)
        plot.plotItem.setLabel(axis='left', units='v')
        plot.setYRange(-3000, 3000)
        # Create the last plot only to keep track of the time (with zeros as q)
        if ch == self.gv.N_CH:
            # Add the label only for the last channel as they all have the same
            plot.plotItem.setLabel(axis='bottom', text='Time', units='s')      # Todo : ALEXM : verifier l'uniter
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
        self.N_CLASSIF_REGIONS_PER_PLOT = 9
        self.regions = Regions(self.gv, self.N_CLASSIF_REGIONS_PER_PLOT)
        for i in range(self.N_CLASSIF_REGIONS_PER_PLOT):
            self.regions.list.append([0, pg.LinearRegionItem([0, 0])])
            plot.addItem(self.regions.list[i][1], ignoreBounds=True)
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
                       color=button_colors[ch], toggle=True, max_width=19,
                       tip=f'Start/Stop the ch{ch+1} signal', max_height=19)
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
        max_width = 17
        max_height = 18
        # Average
        actn_btn = ActionButton(
                self.ch_layout, 0, self.gv, ch, conn_func='avg')
        btn('A', self.ch_layout, (0, 8), action=actn_btn,
            toggle=True, tip='Show average value of queue',
            max_width=max_width, max_height=max_height, color=dark_blue_tab)
        # Max
        actn_btn = ActionButton(
                self.ch_layout, 1, self.gv, ch, conn_func='max')
        btn('M', self.ch_layout, (1, 8), action=actn_btn,
            toggle=True, tip='Show max value of queue',
            max_width=max_width, max_height=max_height, color=dark_blue_tab)
        # Detection
        btn('D', self.ch_layout, (2, 8),
            toggle=True, tip='Show detected class patern',
            max_width=max_width, max_height=max_height, color=dark_blue_tab)

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



