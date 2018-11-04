import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import threading
from collections import deque
from random import random, randint
from math import pi
from numpy import sin
from time import time, sleep
# OpenBCI
import logging
import open_bci_v3 as bci

# My modules


def stream_data_from_OpenBCI(gv):
    port = '/dev/ttyUSB0'  # if using Linux
    # (if encounter error: [Errno 13] could not open port /dev/ttyUSB0: Permission denied => see: https://askubuntu.com/questions/58119/changing-permissions-on-serial-port   then restart your computer
    # port = 'COM3'  # if using Windows
    # port = '/dev/tty.OpenBCI-DN008VTF'  # If using MAC?
    logging.basicConfig(filename="test.log", format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
    logging.info('---------LOG START-------------')
    board = bci.OpenBCIBoard(port=port, scaled_output=False, log=True)
    print("Board Instantiated")
    sleep(5)

    OpenBCI_sampler = SampleDataFromOPENBCI(board, gv)
    OpenBCI_sampler.start()
    
    return board
    
    
class SampleDataFromOPENBCI(threading.Thread):
    def __init__(self, board, gv):
        super().__init__()
        self.board = board
        self.gv = gv
        
    def run(self):
        # Previously and Working
        self.board.start_streaming(self.add_data_to_queue)

    def add_data_to_queue(self, sample):
        for ch, one_sample in enumerate(sample.channel_data):
            self.gv.data_queue[ch].append(one_sample)
            self.gv.all_data[ch].append(one_sample)
        self.gv.n_data_created[0] += 1
        # Time
        current_time = time() - self.gv.t_init
        self.gv.t_queue.append(current_time)
        self.gv.all_t.append(current_time)
        # Add experiment type values
        if self.gv.experiment_type[0] != 0:
            typ = self.gv.experiment_type[0]
            self.gv.experiment_queue.append(typ)
            self.gv.all_experiment_val.append(typ)
            self.gv.experiment_type[0] = 0
        else:
            self.gv.experiment_queue.append(0)
            self.gv.all_experiment_val.append(0)


class CreateData(threading.Thread):
    def __init__(self, gv):
        super().__init__()
        self.gv = gv
        # Variable necessary to generate fake signal
        ## time
        self.t = np.linspace(0, 2 * pi, self.gv.DEQUE_LEN)
        ## signal shape
        self.s1 = sin(self.t)
        self.s2 = sin(20 * self.t)
        self.s3 = sin(40 * self.t)
        self.s4 = 2 * sin(60 * self.t)

    def add_signal_to_queue(self, signal, ch):
        self.gv.data_queue[ch].append(signal)
        self.gv.all_data[ch].append(signal)

    def run(self):
        """Create random data and a time stamp for each of them"""
        while 1:
            self.gv.n_data_created[0] += 1
            i = self.gv.n_data_created[0] % len(self.t)

            for ch in range(self.gv.N_CH):
                rnd_impulse = randint(0, 100)
                # Set impulse size to be added to the signal
                if rnd_impulse == 0:
                    imp = 5
                else:
                    imp = 0
                if ch == 0:
                    signal = self.s1[i] + self.s3[i]+ self.s4[i] + random() + imp
                elif ch == 1:
                    signal = self.s1[i] + 5
                elif ch == 2:
                    signal = self.s2[i]
                elif ch == 3:
                    signal = self.s3[i]
                elif ch == 4:
                    signal = self.s4[i]
                else:
                    signal = random()

                self.add_signal_to_queue(signal, ch)

            # Add current time
            current_t = time() - self.gv.t_init
            self.gv.t_queue.append(current_t)
            self.gv.all_t.append(current_t)

            # Add experiment type values 
            if self.gv.experiment_type[0] != 0:
                self.gv.experiment_queue.append(self.gv.experiment_type[0])
                self.gv.all_experiment_val.append(self.gv.experiment_type[0])
                self.gv.experiment_type[0] = 0
            else:
                self.gv.experiment_queue.append(0)
                self.gv.all_experiment_val.append(0)

            sleep(0.0017)


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
