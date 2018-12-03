import numpy as np
from PyQt5 import QtGui, QtCore


class FreqCalculator:
    def __init__(self, gv, remove_first_data):
        self.gv = gv
        self.remove_first_data = remove_first_data

        self.activated = False
        self.freq_range = 100
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.calcul_frequency)
                                                                               # TODO: ALEXM: Filter instead of removing them direcly like that
    def calcul_frequency(self):
        for ch in range(self.gv.N_CH):
            self.N_DATA = len(self.gv.data_queue[ch])
            self.freq_range = self.get_freq_range(ch)
            self.gv.fft[ch] = self.fft(ch)                            # TODO: ALEXM: Change frequency in function of time

    def get_freq_range(self, ch):
        """Calculate FFT (Remove freq 0 because it gives a really high
         value on the graph"""
        return np.linspace(self.remove_first_data,
                           self.N_DATA//2/self.get_delta_t(),
                           self.N_DATA//2 - self.remove_first_data)

    def get_delta_t(self):
        """interval of time from the first to the last value that was
        add to the queue"""
        return self.gv.t_queue[-1] - self.gv.t_queue[0]

    def fft(self, ch):
        fft = np.fft.fft(self.gv.data_queue[ch])
        return abs(fft[self.remove_first_data:self.N_DATA // 2])
