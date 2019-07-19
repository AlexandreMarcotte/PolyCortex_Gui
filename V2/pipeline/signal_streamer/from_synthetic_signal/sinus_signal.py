import numpy as np


class SinusSignal:
    def __init__(self, amplitude=1, angular_freq=1, phase=0, len=250):
        t = self.init_time(len)
        self.array = amplitude * np.sin(2*np.pi * angular_freq * t + phase)

    def init_time(self, len):
        return np.linspace(0, 1, len, endpoint=False)
