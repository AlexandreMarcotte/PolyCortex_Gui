# -- General Packages --
import re
from time import sleep
from collections import deque
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from functools import partial
from pyqtgraph.dockarea import *
# -- My Packages --
from .ch_number_action import ChNumberAction
from .action_button import ActionButton

from app.colors import *
from app.activation_b import btn
from tabs.region import Regions
from .eeg_graph import EegGraph

from app.pyqt_frequently_used import create_splitter, create_gr

from tabs.live_graph_tab.dock.inner_dock import InnerDock
# -Inner Docks-
from ..eeg_dock.inner_docks.write_hardware_dock import WriteHardwareDock
from ..eeg_dock.inner_docks.banner_dock import BannerDock
from ..eeg_dock.inner_docks.saving_dock import SavingDock
from ..eeg_dock.inner_docks.settings_dock import SettingsDock
from ..eeg_dock.inner_docks.pin_settings_dock import PinsSettingDock
from ..eeg_dock.inner_docks.time_dock import TimeDock

from data_processing_pipeline.frequency_counter import FrequencyCounter
# Generate signal
from generate_signal.from_openbci import SampleDataFromOPENBCI
from generate_signal.from_synthetic_data import CreateSyntheticData
from generate_signal.from_file import FileReader
from generate_signal.from_pcb import PcbReader
# from generate_signal.from_muse import StreamFromMuse


class MainEegDock:
    def __init__(self, gv, layout):
        self.gv = gv
        # General Layout
        self.layout = layout

        self.dock_area = DockArea()
        self.layout.addWidget(self.dock_area, 1, 1, 1, 8)

        self.stream_source = None
        # Regions
        self.N_CLASSIF_REGIONS_PER_PLOT = 9
        self.regions = [Regions(self.gv, self.N_CLASSIF_REGIONS_PER_PLOT)
                        for _ in range(self.gv.N_CH + 1)]
        # Variables
        self.btns = []
        self.ts = self.gv.t_queue
        self.timers = []
        self.plots = []
        self.eeg_graphes = []
        self.zero_q = deque(
                np.zeros(self.gv.DEQUE_LEN), maxlen=self.gv.DEQUE_LEN)
        self.GR_PER_COL = 1

        # Create docks
        SettingsDock(self)
        SavingDock(self)
        WriteHardwareDock(self)
        BannerDock(self)
        pin_settings_dock = PinsSettingDock(self)
        # EEG
        self.grps = self.create_all_eeg_plot()
        self.eeg_dock = self.create_eeg_dock(self.grps)
        # Need to be fully created after the eeg dock is created
        self.settings_pins_d = pin_settings_dock.create_pins_setting_dock()
        # Create time dock
        self.time_dock = TimeDock(self)

    @QtCore.pyqtSlot(bool)
    def start_timers(self, checked):
        self.stream_source = self.init_streaming_source()
        self.gv.stream_source = self.stream_source
        if checked:
            self.freq_counter = FrequencyCounter(
                self.gv, self.gv.stream_origin)
            self.stream_source.start()
            for i, tm in enumerate(self.timers):
                self.timers[i].start(0)
            self.start_freq_counter_timer()
        else:
            for i, tm in enumerate(self.timers):
                self.timers[i].stop()
            # self.stream_source.join()
        # self.set_default_hardware_param()

    def init_streaming_source(self):
        """      """
        if self.gv.stream_origin == 'OpenBCI':
            stream_source = SampleDataFromOPENBCI(self.gv)
        elif self.gv.stream_origin == 'Synthetic data':
            # Create fake data for test case
            stream_source = CreateSyntheticData(
                self.gv, callback=self.gv.collect_data,
                read_freq=1250)
        elif self.gv.stream_origin == 'File':
            stream_source = FileReader(
                self.gv, self.gv.stream_path, self.gv.collect_data,
                read_freq=250)
        elif self.gv.stream_origin == 'Pcb':
            stream_source = PcbReader(
                    self.gv, self.gv.collect_data, read_freq=400)
        else:
            raise('No streaming source selected')

        return stream_source

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
            print("Invalide value")

    def start_freq_counter_timer(self):
        self.freq_counter_timer = QtCore.QTimer()
        self.freq_counter_timer.timeout.connect(self.freq_counter.update)
        self.freq_counter_timer.start(50)

    def change_num_plot_per_row(self, plot_per_row):
        # Eeg dock
        self.eeg_dock.dock.close()
        self.GR_PER_COL = int(plot_per_row)
        self.eeg_dock = self.create_eeg_dock(self.grps)
        # Time dock
        self.dock_area.moveDock(
                self.time_dock.time_d.dock, 'bottom', self.eeg_dock.dock)
        # Hardware settings dock
        self.dock_area.moveDock(
                self.settings_pins_d.dock, 'left', self.eeg_dock.dock)

    @QtCore.pyqtSlot(bool)
    def open_dock(self, dock, checked):
        if checked:
            dock.show()
        else:
            dock.hide()

    def set_saver(self, data_saver):
        self.data_saver = data_saver

    def set_default_hardware_param(self):
        byte_settings = 'x1006110X'
        try:
            for b in byte_settings:
                self.stream_source.board.ser_write(b.encode())
                sleep(0.01)
        except AttributeError as e:
            # Means we are not streaming from the OpenBCI
            print('ERROR', e)

    def create_eeg_dock(self, grps):
        eeg_d = InnerDock(self.layout, 'Part EEG')
        splitters = self.create_splitter(grps)
        s_factor = len(splitters)//self.GR_PER_COL
        for no, s in enumerate(splitters):
            # Add 1 to the row to be in line with the hardware settings
            eeg_d.layout.addWidget(s, no%s_factor, no//s_factor)
        self.dock_area.addDock(eeg_d.dock)
        return eeg_d

    def create_all_eeg_plot(self):
        """
        """
        grps = []
        for ch in range(self.gv.N_CH):
            self.gr, ch_layout = create_gr()
            grps.append(self.gr)
            self.add_ch_layout(ch_layout, ch)
        return grps

    def add_ch_layout(
                self, layout, ch, time_ch=False, plot_pos=(0, 1, 5, 6)):      # TODO: ALEXM: change the name of this function
        plot, q, rowspan = self.create_plot(ch)
        self.plots.append(plot)
        layout.addWidget(plot, *plot_pos)
        curve = self.create_curve(plot, ch, q)
        eeg_graph = EegGraph(ch, q, self.gv, self.ts, curve, self.regions[ch])
        self.eeg_graphes.append(eeg_graph)
        self.timers.append(QtCore.QTimer())
        self.timers[ch].timeout.connect(self.eeg_graphes[ch].update_graph)
        if not time_ch:
            self.assign_n_to_ch(ch, layout)
            self.assign_action_to_ch(ch, layout)

    def create_splitter(self, grps):
        splitters = []
        for i in range(0, len(grps), 2):
            splitter = create_splitter(
                    grps[i], grps[i+1], direction=Qt.Vertical)
            splitters.append(splitter)
        return splitters

    def create_plot(self, ch):
        """Create a plot for all eeg signals and the last to keep
           track of time"""
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

            self.add_classif_regions_to_plot(plot, ch)

        return plot, q, rowspan

    def add_classif_regions_to_plot(self, plot, ch):
        """Create colored region (10) and placed them all at the beginning
           of each plot (will be used to indicated classification of a
           region of the signal or event occured in experiments"""
        for i in range(self.N_CLASSIF_REGIONS_PER_PLOT):
            self.regions[ch].list.append([0, pg.LinearRegionItem([0, 0])])
            plot.addItem(self.regions[ch].list[i][1], ignoreBounds=True)
        return plot

    def create_curve(self, plot, ch, q):
        """Create curves associated with the plots"""
        eeg_curve = plot.plot(self.ts, q)
        eeg_curve.setPen(pen_colors[ch])
        return eeg_curve

    def assign_n_to_ch(self, ch, ch_layout):
        ch_number_action = ChNumberAction(self.timers, ch)
        # +1 so the number str start at 1
        self.btn = btn(
                name=str(ch + 1), layout=ch_layout, pos=(0, 0),
                func_conn=ch_number_action.stop_ch, color=button_colors[ch],
                toggle=True, max_width=19, max_height=19,
                tip=f'Start/Stop the ch{ch+1} signal')
        self.btns.append(self.btn)

    def assign_action_to_ch(self, ch, ch_layout):
        max_width = 17
        max_height = 18
        # Average
        actn_btn = ActionButton(
                ch_layout, 0, self.gv, ch, conn_func='avg')
        btn('A', ch_layout, (0, 8), action=actn_btn,
                toggle=True, tip='Show average value of queue',
                max_width=max_width, max_height=max_height, color=dark_blue_tab,
                txt_color=white)
        # Max
        actn_btn = ActionButton(
                ch_layout, 1, self.gv, ch, conn_func='max')
        btn('M', ch_layout, (1, 8), action=actn_btn,
                toggle=True, tip='Show max value of queue',
                max_width=max_width, max_height=max_height, color=dark_blue_tab,
                txt_color=white)
        # Detection
        actn_btn = ActionButton(
                ch_layout, 2, self.gv, ch, conn_func='filter',
                plot_creator=self)
        btn('F',ch_layout, (2, 8), action=actn_btn,
                toggle=True, tip='''Show the size of the fft window on which
                the fft is calculated for all ch''', max_width=max_width,
                max_height=max_height, color=dark_blue_tab, txt_color=white)

        self.create_color_button(ch, ch_layout)

    def create_color_button(self, ch, ch_layout):
        """Create color button to change the color of the line"""
        color_btn = pg.ColorButton()
        color_btn.setMaximumWidth(17)
        color_btn.setToolTip('Click to change the color of the line')
        color_btn.sigColorChanged.connect(partial(self.change_line_color, ch))
        color_btn.setMaximumHeight(17)
        ch_layout.addWidget(color_btn, 3, 8)

    def change_line_color(self, ch, color_btn):
        color = color_btn.color()
        self.eeg_graphes[ch].curve.setPen(color)
        self.gv.curve_freq[ch].setPen(color)
        self.btns[ch].set_color(color)
