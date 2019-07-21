# --General Packages--
import numpy as np
from collections import deque
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import pyqtSlot


class SignalCollector(QObject):

    filled_new_data_into_queue = pyqtSignal()

    def __init__(self, len=2000, use_reader=False, N_CH=8, event=None):
        super().__init__()

        self.event = event
        # self.input = deque(np.zeros(len), maxlen=len)
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
        # self.input.append(signal[0])
            self.input[ch].append(val)
        # if self.use_reader:
        #     self.reader_queue.append(signal)
        self.timestamps.append(timestamp)

        self.filled_new_data_into_queue.emit()
        # print('n_data_created ', self.n_data_created)

        self.event.set()

    # @pyqtSlot()
    # def print_shit(self):
    #     pass
        # print('shiiiiiiiiiiiiiiiiiiiiiiiiit')



