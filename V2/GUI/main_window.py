import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
from collections import deque
# --My Packages--
from V2.GUI.menu_bar import MenuBar
from V2.GUI.plot_dock import PlotDock
from V2.pipeline.signal_collector import SignalCollector
from V2.pipeline.signal_streamer import SignalStreamer
from V2.pipeline.filter.filter_stage import FilterStage
from V2.pipeline.filter.filter import Filter
from V2.GUI.scroll_plot import ScrollPlot
from V2.pipeline.input_signal.synthetic_signal import SyntheticSignal


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMenuBar(MenuBar())
        # Input signal
        signal_collector = self.start_pipeline()
        self.plot_dock = PlotDock(
                'Input Signal', signals=[signal_collector.signal_deque])
        self.add_dock(self.plot_dock)
        # Filtered signal
        filter_stage = self.start_filter_stage(signal_collector)
        self.filter_signal_dock = PlotDock(
                'Filtered Signal', signals=[filter_stage.input])
        self.add_dock(self.filter_signal_dock)

    def add_dock(self, dock):
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

    def start_pipeline(self):
        signal_collector = SignalCollector(len=2000)
        """Stream and collect"""
        signal_streamer = SignalStreamer(
                input_signal=SyntheticSignal().signal,
                signal_collector=signal_collector, stream_freq=1000)
        signal_streamer.start()
        return signal_collector

    def start_filter_stage(self, signal_collector):
        """Filter"""
        filter = Filter()
        filter_stage = FilterStage(
                input=signal_collector.signal_deque, filter=filter)
        filter_stage.start()
        return filter_stage

