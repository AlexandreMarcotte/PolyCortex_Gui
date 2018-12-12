import numpy as np
from PyQt5 import QtCore
from collections import deque


class FreqCalculator:
    def __init__(self, gv, remove_first_data):
        self.gv = gv
        self.remove_first_data = remove_first_data

        self.freq_per_band_all_ch = [None for _ in range(self.gv.N_CH)]
        self.activated = False
        self.freq_range = 100
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.calcul_frequency)
        self.fft = [None for _ in range(gv.N_CH)]
        self.waves = None
        self.slices = None
        self.N_T_MEMORY = 100
        # I could also just have one deque containing list of all the time stamp
        # each list would contain the 8 values, one for every ch at that time stamp
        self.freq_band_over_time = [
            deque(maxlen=self.N_T_MEMORY) for _ in range(self.gv.N_CH)]
        self.fft_over_time = [deque(maxlen=self.N_T_MEMORY)
                              for _ in range(self.gv.N_CH)]
                                                                               # TODO: ALEXM: Filter instead of removing them direcly like that
    def set_waves(self, waves):
        self.waves = waves
        self.set_slice_for_all_waves()

    def set_slice_for_all_waves(self):
        self.slices = [slice(w.freq_range[0], w.freq_range[1])
                       for w in self.waves.values()]

    def calcul_frequency(self):
        for ch in range(self.gv.N_CH):
            self.N_DATA = len(self.gv.data_queue[ch])
            self.freq_range = self.get_freq_range()
            self.fft[ch] = self.calcul_fft(ch)
            self.fft_over_time[ch].append(self.fft[ch])
            self.freq_per_band_all_ch[ch] = self.get_avg_freq_per_band(ch)

    def get_avg_freq_per_band(self, ch):
        freq_per_band = [np.average(self.fft[ch][s]) for s in self.slices]
        for ch, f in enumerate(freq_per_band):
            self.freq_band_over_time[ch].append(f)
        return freq_per_band

    def get_freq_range(self):
        """Calculate FFT (Remove freq 0 because it gives a really high
         value on the graph"""
        return np.linspace(
                self.remove_first_data, self.N_DATA//2/self.get_delta_t(),
                self.N_DATA//2 - self.remove_first_data)

    def get_delta_t(self):
        """interval of time from the first to the last value that was
        add to the queue"""
        return self.gv.t_queue[-1] - self.gv.t_queue[0]

    def calcul_fft(self, ch):
        fft = np.fft.fft(self.gv.data_queue[ch])
        return abs(fft[self.remove_first_data:self.N_DATA // 2])
