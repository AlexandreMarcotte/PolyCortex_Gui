from collections import deque
import numpy as np
from time import time

class Dispatcher:
    def __init__(self, N_CH=8, DEQUE_LEN=1250, process:list=None):
        self.N_CH = N_CH
        self.DEQUE_LEN = DEQUE_LEN
        self.process = process

        # Variable change in the menubar
        self.stream_origin = 'Stream from synthetic data'

        self.save_path = '_'
        self.used_read_freq = 1000
        self.desired_read_freq = 1000
        self.read_period = 1 / self.desired_read_freq

        self.data_queue = [deque(np.zeros(DEQUE_LEN),
                                 maxlen=DEQUE_LEN) for _ in range(N_CH)]   # One deque per channel initialize at 0

        self.experiment_type = 0
        self.t_queue = deque(np.zeros(self.DEQUE_LEN), maxlen=self.DEQUE_LEN)
        self.experiment_queue = deque(np.zeros(self.DEQUE_LEN), maxlen=self.DEQUE_LEN)
        self.t_init = time()
        self.n_data_created = 1
        # All data
        self.all_data = [deque(np.zeros(self.DEQUE_LEN)) for _ in range(self.N_CH)] 
        self.all_t = deque(np.zeros(self.DEQUE_LEN))
        self.all_experiment_val = deque(np.zeros(self.DEQUE_LEN))
        # Classification
        self.last_classified_type = [0]
        self.emg_signal_len = 170

    def collect_data(self, signal, t, n_data_created):
        """Callback function to use in the generating functions"""
        for ch in range(self.N_CH):
            self.data_queue[ch].append(signal[ch])
            for p in self.process:
                p.data_queue[ch].append(signal[ch])
                # print('append data to process')
        self.t_queue.append(t)
        self.n_data_created = n_data_created

        self.all_data.append(signal)
        self.all_t.append(t)
        # Experiment
        if self.experiment_type != 0:  # An event occured
            self.experiment_queue.append(self.experiment_type)
            self.all_experiment_val.append(self.experiment_type)
            self.experiment_type = 0
        else:
            self.experiment_queue.append(0)
            self.all_experiment_val.append(0)


class FilterProcess:
    def __init__(self, N_CH, DEQUE_LEN):
        self.data_queue = [deque(np.zeros(DEQUE_LEN),
                                 maxlen=DEQUE_LEN) for _ in range(N_CH)]

class VizProcess:
    def __init__(self, N_CH, DEQUE_LEN):
        self.data_queue = [deque(np.zeros(DEQUE_LEN),
                                 maxlen=DEQUE_LEN) for _ in range(N_CH)]


