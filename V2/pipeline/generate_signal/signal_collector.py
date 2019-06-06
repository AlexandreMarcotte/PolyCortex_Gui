# --General Packages--
import numpy as np
from collections import deque


class SignalCollector:
    def __init__(self, len=1000, use_reader=True):
        self.input = deque(np.zeros(len), maxlen=len)
        self.timestamps = deque(np.zeros(len), maxlen=len)
        # Reader
        self.use_reader = use_reader
        self.reader_queue = deque(np.zeros(len))

    def fill_signal_queue(self, signal, timestamp=None):
        """Fill the signal queue with one new signal and its corresponding
        timestamp"""
        print('Signal Collector: fill signal queue')
        self.input.append(signal)
        if self.use_reader:
            self.reader_queue.append(signal)
        self.timestamps.append(timestamp)


