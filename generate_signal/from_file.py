import numpy as np
import threading
from time import time, sleep
import csv


class FileReader(threading.Thread):
    def __init__(self, gv, file_name, collect_data, read_freq=250):
        super().__init__()
        self.gv = gv
        self.file_name = file_name
        self.collect_data = collect_data
        self.gv.read_period = 1/read_freq
        self.gv.used_read_freq = read_freq
        self.gv.desired_read_freq = read_freq

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
                self.collect_data(signal, t=t)
                sleep(self.gv.read_period)


