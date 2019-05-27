from threading import Thread
from queue import Queue
from collections import deque
from abc import abstractclassmethod
import time
from pyqtgraph.Qt import QtGui
# --My Packages--
from V2.GUI.scroll_plot import ScrollPlot


class PipelineStage(Thread):
    def __init__(self, input):
        super().__init__()
        self.input = input

        self.output = deque(input, maxlen=len(input))

        self.daemon = True

    def run(self):
        while True:
            time.sleep(0.0001)  # instead to it every time there is N new value
            self.work()

    @abstractclassmethod
    def work(self):
        """Override this method to create a stage"""
        return

    def show_signal(self, speed=10, show_input=True):
        signals = [self.output]
        if show_input:
            signals.append(self.input)
        """Visualize the output of the stage"""
        self.filtered_plot = ScrollPlot(signals=signals)
        self.filtered_plot.timer.start(speed)


