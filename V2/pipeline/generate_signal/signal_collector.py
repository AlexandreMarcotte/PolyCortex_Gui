# --General Packages--
import numpy as np
from collections import deque


class SignalCollector:
    def __init__(self, len=1000):
        self.input = deque(np.zeros(len), maxlen=len)
        self.timestamps = deque(np.ones(len), maxlen=len)

    def fill_signal_queue(self, signal, timestamp=None):
        self.input.append(signal)
        self.timestamps.append(timestamp)


