import numpy as np


class FreqCalculator:
    def __init__(self, remove_first_data, data_q, t_q):
        self.N_DATA = len(data_q)
        self.data_q = data_q
        self.t_q = t_q

        self.remove_first_data = remove_first_data
                                                                               # TODO: ALEXM: Filter instead of removing them direcly like that
    def get_freq_range(self):
        """Calculate FFT (Remove freq 0 because it gives a really high
         value on the graph"""
        return np.linspace(self.remove_first_data,
                           self.N_DATA//2/self.get_delta_t(),
                           self.N_DATA//2 - self.remove_first_data)

    def get_delta_t(self):
        """interval of time from the first to the last value that was
        add to the queue"""
        return self.t_q[-1] - self.t_q[0]

    def fft(self):
        fft = np.fft.fft(self.data_q)
        return abs(fft[self.remove_first_data:self.N_DATA // 2])
