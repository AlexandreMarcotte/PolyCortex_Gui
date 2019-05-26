# --General Packages--
import numpy as np
from collections import deque


class SignalCollector:
    def __init__(self):
        self.signal_deque = deque(np.ones(1000), maxlen=1000)
        self.i = 0

    def fill_signal_queue(self, signal, timestamp=None):
        self.signal_deque.append(signal)


