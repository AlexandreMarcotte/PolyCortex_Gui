from collections import deque


class FreqBandOverTime:
    def __init__(self, N_WAVE_TYPE, N_T_MEMORY):
        self.wave_type_data = [
            deque(maxlen=N_T_MEMORY) for _ in range(N_WAVE_TYPE)]

    def add_data_to_queue(self, waves_avg):
        for i, val in enumerate(waves_avg):
            self.wave_type_data[i].append(val)
