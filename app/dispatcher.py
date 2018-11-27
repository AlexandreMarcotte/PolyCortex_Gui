from collections import deque
import numpy as np
from time import time
from data_processing_pipeline.filter import butter_bandpass_filter, butter_lowpass_filter


class Dispatcher:
    def __init__(self, N_CH=8, DEQUE_LEN=1250):
        self.N_CH = N_CH
        self.DEQUE_LEN = DEQUE_LEN

        self.filter_process = FilterProcess(N_CH=N_CH, DEQUE_LEN=DEQUE_LEN)
        self.filter_itt = 0
        self.once_every = 20
        self.filter_chunk = []
        self.use_filter = True
        self.N_DATA_BEFORE_FILTER = 1000

        # Variable change in the menubar
        self.stream_origin = 'Stream from synthetic data'
        self.stream_path = f'experiment_csv/2exp_pinch_close_2018-08-29 18:55:22.627296.csv'

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
        self.n_data_created = 0
        # All data
        self.all_data = [deque(np.zeros(self.DEQUE_LEN)) for _ in range(self.N_CH)] 
        self.all_t = deque(np.zeros(self.DEQUE_LEN))
        self.all_experiment_val = deque(np.zeros(self.DEQUE_LEN))
        # Classification
        self.last_classified_type = [0]
        self.emg_signal_len = 170

    def collect_data(self, signal, t=None):
        """Callback function to use in the generating functions"""
        if self.stream_origin == 'Stream from OpenBCI':
            signal = signal.channel_data
        if not t:
            t = time()

        self.filter_itt += 1
        for ch in range(self.N_CH):
            if self.use_filter and self.n_data_created > self.N_DATA_BEFORE_FILTER:
                self.filter_data(ch, signal)
            else:
                self.data_queue[ch].append(signal[ch])

            self.all_data[ch].append(self.data_queue[ch][-1])

        self.t_queue.append(t)
        self.all_t.append(t)
        # Experiment
        if self.experiment_type != 0:  # An event occured
            self.experiment_queue.append(self.experiment_type)
            self.all_experiment_val.append(self.experiment_type)
            self.experiment_type = 0
        else:
            self.experiment_queue.append(0)
            self.all_experiment_val.append(0)

        self.n_data_created += 1

    def filter_data(self, ch, signal):                                       # TODO: ALEXM: I tried to put that into a class 2 times and it made the filtering look weird (try again)
        self.filter_process.data_queue[ch].append(signal[ch])

        if self.filter_itt % self.once_every == 0:
            y = butter_bandpass_filter(self.filter_process.data_queue[ch],     # TODO: ALEXM: There is a problem when the filtering of a bandpass filter filter all 0 it increase the signal to infinity
                                       2, 45, self.desired_read_freq, order=3)
            self.filter_chunk.append(list(y[-self.once_every:][::-1]))
        # put the data once at the time at every loop so the signal is not showing
        # all jerky
        if any(self.filter_chunk):
            val = self.filter_chunk[ch].pop()
            self.data_queue[ch].append(val)
            # print(len(self.all_data[ch]))
            # When you removed the last one init the list again to []
            # So that there is not many void list inside of the main list
            if not any(self.filter_chunk):
                self.filter_chunk = []


class FilterProcess:
    def __init__(self, N_CH, DEQUE_LEN):
        self.data_queue = [deque(np.zeros(DEQUE_LEN),
                                 maxlen=DEQUE_LEN) for _ in range(N_CH)]



