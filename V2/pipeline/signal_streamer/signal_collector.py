# --General Packages--
import numpy as np
from collections import deque
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import pyqtSlot


class SignalCollector(QObject):

    filled_new_data_into_queue = pyqtSignal()

    def __init__(self, len=2000, use_reader=False, N_CH=8, filter_stage=None):
        super().__init__()

        self.filter_stage = filter_stage

        self.n_data_created = 0
        self.input = [deque(np.zeros(len), maxlen=len)
                      for _ in range(8)]

        self.timestamps = deque(np.zeros(len), maxlen=len)
        # Reader
        self.use_reader = use_reader
        self.reader_queue = deque(np.zeros(len))

    def fill_signal_queue(self, signal, timestamp=None):
        """Fill the signal queue with one new signal and its corresponding
        timestamp"""

        self.n_data_created += 1
        for ch, val in enumerate(signal):
            self.input[ch].append(val)

        # Filter data
        self.filter_stage.work(self.input)

        self.timestamps.append(timestamp)


