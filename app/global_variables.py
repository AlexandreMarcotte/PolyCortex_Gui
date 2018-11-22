from collections import deque
import numpy as np
from time import time

class GlobVar:
    def __init__(self):
        self.save_path = '_'
        self.N_CH = 8
        self.DEQUE_LEN = 1250

        self.used_read_freq = 1000
        self.desired_read_freq = 1000
        self.read_period = 1 / self.desired_read_freq

        self.data_queue = [deque(np.zeros(self.DEQUE_LEN),
                           maxlen=self.DEQUE_LEN) for _ in range(self.N_CH)]   # One deque per channel initialize at 0
        self.experiment_type = 0
        self.t_queue = deque(np.zeros(self.DEQUE_LEN), maxlen=self.DEQUE_LEN)
        self.experiment_queue = deque(np.zeros(self.DEQUE_LEN), maxlen=self.DEQUE_LEN)
        self.t_init = time()
        self.n_data_created = 1
        # All data
        self.all_data = [deque(np.zeros(self.DEQUE_LEN)) for _ in range(self.N_CH)] 
        self.all_t = deque(np.zeros(self.DEQUE_LEN))
        self.all_experiment_val = deque(np.zeros(self.DEQUE_LEN))
        # Variable change in the menubar
        self.stream_origin = 'Stream from synthetic data'
        # Classification
        self.last_classified_type = [0]
        self.emg_signal_len = 170

    def collect_data(self, signal, t, n_data_created):
        """Callback function to use in the generating functions"""
        for ch in range(self.N_CH):
            self.data_queue[ch].append(signal[ch])
        self.t_queue.append(t)
        self.n_data_created = n_data_created

        self.all_data.append(signal)
        self.all_t.append(t)


