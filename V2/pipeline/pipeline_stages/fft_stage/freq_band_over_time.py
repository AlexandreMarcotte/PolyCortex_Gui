from collections import deque
import numpy as np


class FreqBandOverTime:
    def __init__(self, N_WAVE_TYPE, N_T_MEMORY=100):
        self.wave_type_data = [
            deque(np.array([0]), maxlen=N_T_MEMORY) for _ in range(N_WAVE_TYPE)]

    def add_data_to_queue(self, waves_avg):
        for i, val in enumerate(waves_avg):
            self.wave_type_data[i].append(val)
