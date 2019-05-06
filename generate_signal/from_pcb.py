import serial
import threading
from time import sleep
from time import time
import numpy as np


class PcbReader(threading.Thread):
    def __init__(self, gv, collect_data, read_freq):
        super().__init__()
        self.gv = gv
        self.read_freq = read_freq
        self.read_period = 1/read_freq
        self.collect_data = collect_data

        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.5)

    def run(self):
        self.read()

    def read(self):
        t_init = time()
        while True:
            signal = np.zeros(8)
            for ch in range(4):
                byte_signal = self.ser.readline()
                print('sig', byte_signal)
                try:
                    signal[ch] = int(byte_signal[:-2])
                    # If list of value
                    # byte_signal = byte_signal.split(sep=',')
                    # for no, ch_val in enumerate(byte_signal):
                    #     signal[no] = int(ch_val)
                except ValueError as e:
                    print(e)
                    print('byte_signal not valid: ', byte_signal)
                # print(self.ser.readline())
                t = time() - t_init
                self.collect_data(signal, t=t)

                # sleep(self.read_period)


    if __name__ == '__main__':
        # ser_reader = SerialReader()
        # ser_reader.start()
        pass

    """
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
            # signal = np.array([float(val) for val in line[:8]])
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.5)
            print(ser.read())
            # t = time() - t_init
            # self.collect_data(signal, t=t)
            sleep(self.gv.read_period)
    """
