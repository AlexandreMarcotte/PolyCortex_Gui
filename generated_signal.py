import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import threading
from collections import deque
from random import random, randint
from frequency_counter import FrequencyCounter
from math import pi
from numpy import sin
from time import time, sleep
# OpenBCI
import logging
import open_bci_v3 as bci


def stream_data_from_OpenBCI(data_queue, t_queue, t_init, n_data_created): 
    port = '/dev/ttyUSB0'  # if using Linux
    # (if encounter error: [Errno 13] could not open port /dev/ttyUSB0: Permission denied => see: https://askubuntu.com/questions/58119/changing-permissions-on-serial-port   then restart your computer
    # port = 'COM3'  # if using Windows
    # port = '/dev/tty.OpenBCI-DN008VTF'  # If using MAC?
    logging.basicConfig(filename="test.log", format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
    logging.info('---------LOG START-------------')
    board = bci.OpenBCIBoard(port=port, scaled_output=False, log=True)
    print("Board Instantiated")
    sleep(5)

    OpenBCI_sampler = SampleDataFromOPENBCI(board, data_queue, t_queue, t_init,
                                            n_data_created)
    OpenBCI_sampler.start()
    
    return board
    
    
class SampleDataFromOPENBCI(threading.Thread):
    def __init__(self, board, data_queue, t_queue, t_init, n_data_created):
        super(SampleDataFromOPENBCI, self).__init__()
        self.board = board
        self.data_queue = data_queue
        self.t_queue = t_queue
        self.t_init = t_init
        self.n_data_created = n_data_created
        
    def run(self):
        self.board.start_streaming(self.add_data_to_queue)
        
    def add_data_to_queue(self, sample):
        for ch, one_sample in enumerate(sample.channel_data):
            self.data_queue[ch].append(one_sample)
        self.n_data_created[0] += 1
        # print('n_data_created', self.n_data_created)
        self.t_queue.append(time() - self.t_init)


class CreateData(threading.Thread):
    def __init__(self, data_queue, t_queue, t_init, n_data_created):
        super(CreateData, self).__init__()
        self.data_queue = data_queue
        self.t_queue = t_queue
        self.t_init = t_init
        self.N_Ch = 8
        self.N_DATA = len(self.data_queue[0])
        self.n_val_created = n_data_created
        self.freq_counter = FrequencyCounter(loop_name='creatingFakeData')
        self.t = np.linspace(0, 2 * pi, self.N_DATA)
        self.s1 = sin(self.t)
        self.s2 = sin(20 * self.t)
        self.s3 = sin(40 * self.t)
        self.s4 = 2 * sin(60 * self.t)

    def run(self):
        """Create random data and a time stamp for each of them"""
        while 1:
            self.n_val_created[0] += 1
            self.i = self.n_val_created[0] % len(self.t)
            # Print frequency of the run function once every second
            self.freq_counter.print_freq(self.n_val_created[0])
            for ch in range(self.N_Ch):
                rnd_impulse = randint(0, 100)
                if rnd_impulse == 0:
                    imp = 5
                else:
                    imp = 0
                if ch == 0:
                    self.data_queue[ch].append(self.s1[self.i] + self.s3[self.i]
                                             + self.s4[self.i] + random() + imp)
                elif ch == 1: 
                    self.data_queue[ch].append(self.s1[self.i] + 5)
                elif ch == 2:
                    self.data_queue[ch].append(self.s2[self.i])
                elif ch == 3: 
                    self.data_queue[ch].append(self.s3[self.i])
                elif ch == 4: 
                    self.data_queue[ch].append(self.s4[self.i])
                else: 
                    self.data_queue[ch].append(random())

            self.t_queue.append(time() - self.t_init)
            sleep(0.0017)


class CreateDataFromFile(threading.Thread):
    def __init__(self, data_queue, t_queue, t_init, n_data_created):
        super(CreateDataFromFile, self).__init__()
        self.data_queue = data_queue
        self.n_data_created = n_data_created
        self.t_queue = t_queue
        self.t_init = t_init
        self.N_DATA = len(self.data_queue)

    def run(self):
        self.write_to_file()

    def write_to_file(self):
        with open('csv_eeg_data.csv', 'r') as f:
            for all_ch_line in f:
                self.n_data_created[0] += 1
                all_ch_line = all_ch_line.strip().split(',')
                for ch_no, ch in enumerate(all_ch_line):
                    self.data_queue[ch_no].append(float(ch))

                self.t_queue.append(time() - self.t_init)
                sleep(0.004)


def read_data_from_file(file_name, n_ch):
    n_data = 0
    # Count the total number of data point
    with open(file_name, 'r') as f:
        for _ in f:
            n_data += 1

    print('n_data', n_data)
    # Create the data structure as a deque
    data = [deque(np.zeros(n_data),
                  maxlen=n_data) for _ in range(n_ch)]

    # Read all the lines in the file and add them to the data deque
    with open(file_name, 'r') as f:
        for all_ch_line in f:
            all_ch_line = all_ch_line.strip().split(',')
            for ch_no, ch in enumerate(all_ch_line):
                data[ch_no].append(float(ch))
    return data
