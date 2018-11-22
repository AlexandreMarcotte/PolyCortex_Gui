import numpy as np
import threading
from collections import deque
from time import time, sleep
import csv


class FileReader(threading.Thread):
    def __init__(self, gv, file_name, callback, read_freq=250):
        super().__init__()
        self.gv = gv
        self.file_name = file_name
        self.callback = callback
        self.gv.read_period = 1/read_freq
        self.gv.used_read_freq = read_freq
        self.gv.desired_read_freq = read_freq

        self.n_data_created = 0

    def run(self):
        self.read()

    def read(self):
        t_init = time()
        print(self.file_name)
        with open(self.file_name) as f:
            data = csv.reader(f)
            for line in data:
                signal = np.array([float(val) for val in line[:8]])
                t = time() - t_init
                self.n_data_created += 1
                self.callback(signal, t, self.n_data_created)
                sleep(self.gv.read_period)


# Used in the tab 3 where we create static graphes
def read_data_from_file(file_name, n_ch=8):
    n_data = 0
    # Count the total number of data point
    with open(file_name, 'r') as f:
        for _ in f:
            n_data += 1

    print('n_data', n_data)
    # Create the data structure as a deque
    data = [deque(np.zeros(n_data), maxlen=n_data) for _ in range(n_ch)]
    t = deque(np.zeros(n_data), maxlen=n_data)
    exp = deque(np.zeros(n_data), maxlen=n_data)

    # Read all the lines in the file and add them to the data deque
    with open(file_name, 'r') as f:
        for all_ch_line in f:
            all_ch_line = all_ch_line.strip().split(',')                       # TODO: ALEXM read the file as a csv instead
            eeg_ch = all_ch_line[0:8]
            t.append(float(all_ch_line[8:9][0]))
            exp.append(float(all_ch_line[9:10][0]))
            for ch_no, ch in enumerate(eeg_ch):
                data[ch_no].append(float(ch))
    return data, t, exp
