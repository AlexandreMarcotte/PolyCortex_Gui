from threading import Thread
from queue import Queue
from collections import deque
from abc import abstractclassmethod
import time
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg
# --My Packages--
from V2.GUI.scroll_plot_widget import ScrollPlotWidget
from PyQt5.QtWidgets import *


class PipelineStage(Thread):
    def __init__(self, input, show_signal=False):
        super().__init__()
        self.input = input

        self.output = deque(input, maxlen=len(input))

        self.daemon = True

        if show_signal:
            self.show_signal()

    def run(self):
        while True:
            self.work()
            time.sleep(0.02)  # instead to it every time there is N new value

    @abstractclassmethod
    def work(self):
        """Override this method to create a stage"""
        return

    def show_signal(self):
        win = pg.GraphicsWindow()

        signals = [self.output]
        """Visualize the output of the stage"""
        self.filtered_plot = ScrollPlotWidget(signals=signals)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.filtered_plot)
        win.setCentralWidget(self.layout)
