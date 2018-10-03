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

# My modules
from init_variables import InitVariables


def stream_data_from_OpenBCI(data_queue, t_queue, experiment_queue,
                             experiment_type, t_init, n_data_created,
                             all_data, all_t, all_experiment_val):
    port = '/dev/ttyUSB0'  # if using Linux
    # (if encounter error: [Errno 13] could not open port /dev/ttyUSB0: Permission denied => see: https://askubuntu.com/questions/58119/changing-permissions-on-serial-port   then restart your computer
    # port = 'COM3'  # if using Windows
    # port = '/dev/tty.OpenBCI-DN008VTF'  # If using MAC?
    logging.basicConfig(filename="test.log", format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
    logging.info('---------LOG START-------------')
    board = bci.OpenBCIBoard(port=port, scaled_output=False, log=True)
    print("Board Instantiated")
    sleep(5)

    OpenBCI_sampler = SampleDataFromOPENBCI(board, data_queue, experiment_queue,
                                            experiment_type,t_queue, t_init,
                                            n_data_created, all_data, all_t,
                                            all_experiment_val)
    OpenBCI_sampler.start()
    
    return board
    
    
class SampleDataFromOPENBCI(threading.Thread):
    def __init__(self, board, data_queue, experiment_queue, experiment_type,
                 t_queue, t_init, n_data_created, all_data, all_t, all_experiment_val):
        super().__init__()
        self.board = board

        # Queue
        self.data_queue = data_queue
        self.t_queue = t_queue
        # All data for saving
        self.all_data = all_data
        self.all_t = all_t
        self.all_experiment_val = all_experiment_val

        self.t_init = t_init
        self.n_data_created = n_data_created
        self.experiment_queue = experiment_queue
        self.experiment_type = experiment_type 
        
    def run(self):
        # Previously and Working
        self.board.start_streaming(self.add_data_to_queue)

    def add_data_to_queue(self, sample):
        for ch, one_sample in enumerate(sample.channel_data):
            self.data_queue[ch].append(one_sample)
            self.all_data[ch].append(one_sample)
        self.n_data_created[0] += 1
        # Time
        current_time = time() - self.t_init
        self.t_queue.append(current_time)
        self.all_t.append(current_time)
        # Add experiment type values
        if self.experiment_type[0] != 0:
            typ = self.experiment_type[0]
            self.experiment_queue.append(typ)
            self.all_experiment_val.append(typ)
            self.experiment_type[0] = 0
        else:
            self.experiment_queue.append(0)
            self.all_experiment_val.append(0)


class CreateData(threading.Thread, InitVariables):
    def __init__(self, data_queue, t_queue, experiment_queue, experiment_type,
                 t_init, n_data_created, all_data, all_t, all_experiment_val):
        super().__init__()
        # Queue
        self.data_queue = data_queue
        self.t_queue = t_queue
        self.experiment_queue = experiment_queue
        # All data for saving
        self.all_data = all_data
        self.all_t = all_t
        self.all_experiment_val = all_experiment_val

        self.experiment_type = experiment_type

        self.t_init = t_init
        self.N_CH = 8
        self.N_DATA = len(self.data_queue[0])
        self.n_val_created = n_data_created
        self.freq_counter = FrequencyCounter(loop_name='creatingFakeData')
        self.t = np.linspace(0, 2 * pi, self.N_DATA)
        self.s1 = sin(self.t)
        self.s2 = sin(20 * self.t)
        self.s3 = sin(40 * self.t)
        self.s4 = 2 * sin(60 * self.t)

    def add_signal_to_queue(self, signal, ch):
        self.data_queue[ch].append(signal)
        self.all_data[ch].append(signal)

    def run(self):
        """Create random data and a time stamp for each of them"""
        while 1:
            self.n_val_created[0] += 1
            self.i = self.n_val_created[0] % len(self.t)
            # Print frequency of the run function once every second
            self.freq_counter.print_freq(self.n_val_created[0])
            for ch in range(self.N_CH):
                rnd_impulse = randint(0, 100)
                if rnd_impulse == 0:
                    imp = 5
                else:
                    imp = 0
                if ch == 0:
                    signal = self.s1[self.i] + self.s3[self.i] \
                             + self.s4[self.i] + random() + imp
                elif ch == 1:
                    signal = self.s1[self.i] + 5
                elif ch == 2:
                    signal = self.s2[self.i]
                elif ch == 3:
                    signal = self.s3[self.i]
                elif ch == 4:
                    signal = self.s4[self.i]
                else:
                    signal = random()

                self.add_signal_to_queue(signal, ch)

            # Add current time
            current_t = time() - self.t_init
            self.t_queue.append(current_t)
            self.all_t.append(current_t)

            # Add experiment type values 
            if self.experiment_type[0] != 0:
                self.experiment_queue.append(self.experiment_type[0])
                self.all_experiment_val.append(self.experiment_type[0])
                self.experiment_type[0] = 0
            else:
                self.experiment_queue.append(0)
                self.all_experiment_val.append(0)

            sleep(0.0017)


class CreateDataFromFile(threading.Thread):
    def __init__(self, data_queue, t_queue, t_init, n_data_created, file_name):
        super(CreateDataFromFile, self).__init__()
        self.data_queue = data_queue
        self.n_data_created = n_data_created
        self.t_queue = t_queue
        self.t_init = t_init
        self.N_DATA = len(self.data_queue)
        self.file_name = file_name

    def run(self):
        self.write_to_file()

    def write_to_file(self):
        with open(self.file_name, 'r') as f:
            for all_ch_line in f:
                self.n_data_created[0] += 1
                all_ch_line = all_ch_line.strip().split(',')[0:8]
                for ch_no, ch in enumerate(all_ch_line):
                    self.data_queue[ch_no].append(float(ch))

                self.t_queue.append(time() - self.t_init)
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
