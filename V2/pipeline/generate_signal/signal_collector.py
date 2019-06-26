# --General Packages--
import numpy as np
from collections import deque


class SignalCollector:
    def __init__(self, len=1000, use_reader=False, N_CH=8):
        # self.input = deque(np.zeros(len), maxlen=len)
        self.input = [deque(np.zeros(len), maxlen=len)
                      for _ in range(8)]

        self.timestamps = deque(np.zeros(len), maxlen=len)
        # Reader
        self.use_reader = use_reader
        self.reader_queue = deque(np.zeros(len))

    def fill_signal_queue(self, signal, timestamp=None):
        """Fill the signal queue with one new signal and its corresponding
        timestamp"""
        for ch, val in enumerate(signal):
        # self.input.append(signal[0])
            self.input[ch].append(val)
        # if self.use_reader:
        #     self.reader_queue.append(signal)
        self.timestamps.append(timestamp)


