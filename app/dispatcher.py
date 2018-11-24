from collections import deque
import numpy as np
from time import time
from data_processing_pipeline.filter import butter_bandpass_filter, butter_lowpass_filter


class Dispatcher:
    def __init__(self, N_CH=8, DEQUE_LEN=1250,
                 filter_process=None, viz_process=None):
        self.N_CH = N_CH
        self.DEQUE_LEN = DEQUE_LEN

        self.filter_process = filter_process
        self.filter_itt = 0
        self.once_every = 30
        self.filter_chunk = []
        self.use_filter = True
        self.viz_process = viz_process

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
        self.filter_itt += 1
        for ch in range(self.N_CH):
            if self.use_filter:
                self.filter_process.data_queue[ch].append(signal[ch])

                if self.filter_itt % self.once_every == 0:
                    y = butter_bandpass_filter(self.filter_process.data_queue[ch],  # TODO: ALEXM: There is a problem when the filtering of a bandpass filter filter all 0 it increase the signal to infinity
                                              10, 50, self.desired_read_freq, order=6)
                    self.filter_chunk.append(list(y[-self.once_every:][::-1]))
                # put the data once at the time at every loop so the signal is not showing
                # all jerky
                if any(self.filter_chunk):
                    val = self.filter_chunk[ch].pop()
                    self.data_queue[ch].append(val)
                    # When you removed the last one init the list again to []
                    # So that there is not many void list inside of the main list
                    if not any(self.filter_chunk):
                        self.filter_chunk = []
            else:
                self.data_queue[ch].append(signal[ch])

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
        self.name = 'filter'
        self.data_queue = [deque(np.zeros(DEQUE_LEN),
                                 maxlen=DEQUE_LEN) for _ in range(N_CH)]

class VizProcess:
    def __init__(self, N_CH, DEQUE_LEN):
        self.name = 'viz'
        self.data_queue = [deque(np.zeros(DEQUE_LEN),
                                 maxlen=DEQUE_LEN) for _ in range(N_CH)]


