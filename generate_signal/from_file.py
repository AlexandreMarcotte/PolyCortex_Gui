import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import threading
from collections import deque
from time import time, sleep


class CreateDataFromFile(threading.Thread):
    def __init__(self, gv, file_name):
        super(CreateDataFromFile, self).__init__()
        self.gv = gv
        self.N_DATA = len(self.gv.data_queue)
        self.file_name = file_name

    def run(self):
        self.write_to_file()

    def write_to_file(self):
        with open(self.file_name, 'r') as f:
            for all_ch_line in f:
                self.gv.n_data_created[0] += 1
                all_ch_line = all_ch_line.strip().split(',')[0:8]
                for ch_no, ch in enumerate(all_ch_line):
                    self.gv.data_queue[ch_no].append(float(ch))

                self.gv.t_queue.append(time() - self.gv.t_init)
                sleep(0.002) # TODO: ALEXM this delta t could be calculated from the saved time in the file

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
            all_ch_line = all_ch_line.strip().split(',')
            eeg_ch = all_ch_line[0:8]
            t.append(float(all_ch_line[8:9][0]))
            exp.append(float(all_ch_line[9:10][0]))
            for ch_no, ch in enumerate(eeg_ch):
                data[ch_no].append(float(ch))
    return data, t, exp
