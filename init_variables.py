from collections import deque
import numpy as np
from time import time

class InitVariables:
    def __init__(self):
        self.N_CH = 8
        self.DEQUE_LEN = 1250

        self.data_queue = [deque(np.zeros(self.DEQUE_LEN),
                           maxlen=self.DEQUE_LEN) for _ in range(self.N_CH)]   # One deque per channel initialize at 0
        self.experiment_type = [0]
        self.t_queue = deque(np.zeros(self.DEQUE_LEN), maxlen=self.DEQUE_LEN)
        self.experiment_queue = deque(np.zeros(self.DEQUE_LEN), maxlen=self.DEQUE_LEN)
        self.t_init = time()
        self.n_data_created = [1]
        # All data
        self.all_data = [deque(np.zeros(self.DEQUE_LEN)) for _ in range(self.N_CH)] 
        self.all_t = deque(np.zeros(self.DEQUE_LEN))
        self.all_experiment_val = deque(np.zeros(self.DEQUE_LEN))
        # Variable change in the menubar
        self.stream_origin = ['Stream fake data']
