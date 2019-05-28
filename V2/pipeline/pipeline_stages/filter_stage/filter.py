from scipy.signal import butter, lfilter


class Filter:
    def __init__(self, cut_freq=(50, 70), stream_freq=1000, order=3,
                 filter_type='bandstop'):
        self.cut_freq = cut_freq
        self.stream_freq = stream_freq
        self.order = order
        self.filter_type = filter_type

        self.coeff = self.set_filter_coeff()

    def set_filter_coeff(self):
        nyq = 0.5 * self.stream_freq
        normalized_cut_freq = [coeff/nyq for coeff in self.cut_freq]
        coeff = butter(
                N=self.order, Wn=normalized_cut_freq, btype=self.filter_type,
                analog=False)
        return coeff

    def filter_signal(self, input):
        return lfilter(self.coeff[0], self.coeff[1], input)

