import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import threading
# from Queue import Queue
import time
from random import random
from frequency_counter import FrequencyCounter
from math import pi
from numpy import sin


class CreateData(threading.Thread):
    def __init__(self, data_queue, n_data_created):
        super(CreateData, self).__init__()
        self.data_queue = data_queue
        self.N_Ch = 8
        self.N_data = len(self.data_queue[0])
        self.n_val_created = n_data_created
        self.freq_counter = FrequencyCounter(loop_name='creatingFakeData')
        self.t = np.linspace(0, 2 * pi, self.N_data)
        self.s1 = sin(self.t)
        self.s2 = sin(2 * self.t)
        self.s3 = sin(5 * self.t)
        self.s4 = sin(10 * self.t)

    def run(self):
        """Create random data and a time stamp for each of them"""
        while 1:
            self.n_val_created[0] += 1
            self.i = self.n_val_created[0] % len(self.t)
            # Print frequency of the run function once every second
            self.freq_counter.print_freq(self.n_val_created[0])
            for ch in range(self.N_Ch):
                self.data_queue[ch].append(self.s1[self.i] + self.s3[self.i]
                                         + self.s4[self.i] + random())
            time.sleep(0.004)


class CreateDataFromFile(threading.Thread):
    def __init__(self, data_queue):
        super(CreateDataFromFile, self).__init__()
        self.data_queue = data_queue
        self.N_DATA = len(self.data_queue)

    def run(self):
        self.write_to_file()

    def write_to_file(self):
        with open('csv_eeg_data.csv', 'r') as f:
            for all_ch_line in f:
                all_ch_line = all_ch_line.strip().split(',')
                for ch_no, ch in enumerate(all_ch_line):
                    self.data_queue[ch_no].append(float(ch))
                time.sleep(0.004)

