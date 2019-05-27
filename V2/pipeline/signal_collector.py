# --General Packages--
import numpy as np
from collections import deque


class SignalCollector:
    def __init__(self, len=1000):
        self.signal_deque = deque(np.ones(len), maxlen=len)
        self.i = 0

    def fill_signal_queue(self, signal, timestamp=None):
        self.signal_deque.append(signal)


