import numpy as np
import threading
from time import time, sleep
import csv


class FileStreamer(threading.Thread):
    def __init__(self, file_name, signal_collector, stream_freq=250):
        super().__init__()
        self.file_name = file_name
        self.signal_collector = signal_collector
        self.stream_period = 1/stream_freq

        self.start()

    def run(self):
        self.stream_from_file()

    def stream_from_file(self):
        t_init = time()
        print('Stream from: ', self.file_name)
        with open(self.file_name) as f:
            data = csv.reader(f)
            for line in data:
                # signal = np.array([float(val) for val in line[:8]])
                signal = float(line[0])
                timestamp = time() - t_init
                self.signal_collector.fill_signal_queue(
                    signal, timestamp=timestamp)
                sleep(self.stream_period)


