import numpy as np


class SinusSignal:
    def __init__(self, amplitude=1, angular_freq=1, phase=0):
        t = self.init_time()
        self.array = amplitude * np.sin(angular_freq * t + phase)

    def init_time(self):
        return np.linspace(0, 2 * np.pi, 100)[:-1]  # remove last value as
                                                    # first and last value are
                                                    # the same
