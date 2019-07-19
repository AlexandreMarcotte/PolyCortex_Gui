# --General Imports--
from scipy.signal import butter, lfilter
# --My Packages--
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.filter_region import FilterRegion


class Filter:
    def __init__(self, cut_freq:[50, 70], stream_freq=250, order=3,
                 filter_type='bandstop'):
        self.cut_freq = cut_freq
        self.stream_freq = stream_freq
        self.order = order
        self.filter_type = filter_type

        self.coeff = self.set_filter_coeff(cut_freq[0], cut_freq[1])

    def set_filter_coeff_from_filter_region(self, filter_region:FilterRegion):
        # print('min_bound', filter_region.min_boundary,
        #       'max_bound', filter_region.max_boundary)
        self.coeff = self.set_filter_coeff(
            filter_region.min_boundary, filter_region.max_boundary)

    def set_filter_coeff(self, min_bound, max_bound):
        nyq = 0.5 * self.stream_freq
        normalized_cut_freq = [coeff/nyq for coeff in (min_bound, max_bound)]
        coeff = butter(
                N=self.order, Wn=normalized_cut_freq, btype=self.filter_type,
                analog=False)
        return coeff

    def filter_signal(self, input):
        return lfilter(self.coeff[0], self.coeff[1], input)

