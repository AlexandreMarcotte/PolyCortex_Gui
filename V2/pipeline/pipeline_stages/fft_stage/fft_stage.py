# --General Packages--
import numpy as np
from collections import deque
# --My Packages--
from V2.pipeline.pipeline_stages.pipeline_stage import PipelineStage
from .freq_band_over_time import FreqBandOverTime
from V2.utils.waves import waves


class FftStage(PipelineStage):
    def __init__(self, input, timestamps, remove_first_freq=1, n_ch=8):
        self.len_deque = len(input[0])
        super().__init__(self.len_deque, stream_period=0.2)

        self._n_ch = n_ch
        # The output needs to be half the length because of the fft
        self.output = [deque(input[0], maxlen=self.len_deque//2)
                       for _ in range(len(input))]
        self.input = input
        self.timestamps = timestamps
        # self.remove_first_freq = remove_first_freq

        self.freq_range = np.ones(self.len_deque//2)

        self.N_T_MEMORY = 100
        self.fft_over_time = [
            deque(maxlen=self.N_T_MEMORY) for _ in range(n_ch)]

        # -------- Power band ---------
        self.freq_per_band_all_ch = [None for _ in range(n_ch)]
        self.slices = None
        self._set_waves(waves)
        # ------------------------------

    def work(self):
        self.freq_range = self._get_freq_range(self.len_deque)
        for ch, input in enumerate(self.input):
            self.output[ch] = self._calcul_fft(input)
            # keep track of fft values over time
            self.fft_over_time[ch].append(self.output[ch])
            self.freq_per_band_all_ch[ch] = self.get_avg_freq_per_band(ch)

    def _calcul_fft(self, queue):
        fft = np.fft.fft(queue)
        # Take the abs value to be in the Reel domain
        output = abs(fft[:len(queue)//2])
        return output

    def _get_freq_range(self, n_data):
        """Calculate FFT (Remove freq 0 because it gives a really high
         value on the graph"""
        # Remove the opposite side of the fft which is a symmetry
        delta_t = self._get_delta_t()
        # To make sure there is no zero division
        if delta_t == 0:
            delta_t = 0.00001
            print('fft_stage zero')
        freq_range = np.linspace(0, n_data//2/delta_t, n_data//2)
        return freq_range

    def _get_delta_t(self):
        """interval of time from the first to the last value that was
        add to the queue"""
        return self.timestamps[-1] - self.timestamps[0]

    # ------for Power band plot------
    def _set_waves(self, waves):
        self.waves = waves
        self.set_slice_for_all_waves()
        self.all_freq_band_over_time = [
            FreqBandOverTime(len(self.waves.values()),
                             N_T_MEMORY=self.N_T_MEMORY)
            for _ in range(self._n_ch)]

    def set_slice_for_all_waves(self):
        self.slices = [[w.freq_range[0], w.freq_range[1]]
                        for w in self.waves.values()]
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!Warning !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def get_avg_freq_per_band(self, ch):
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # TODO: ALEXM IMPROVE the frequency is not properly calculated
        # use the last value of: self.fft_stage.freq_range
        # pour faire un produit croisé
        # the slice is over the array and not over the frequency range
        # Scale factor to have right frequency to len of deque ratio
        scale_factor = self.len_deque / self.freq_range[-1]
        scaled_slices = []

        for s in self.slices:
            min_bound, max_bound = s
            scaled_slices.append([int(min_bound * scale_factor),
                                  int(max_bound * scale_factor)])
        freq_per_band = [
            np.average(self.output[ch][
                           slice(*s)]) for s in scaled_slices]

        self.all_freq_band_over_time[ch].add_data_to_queue(freq_per_band)

        return freq_per_band



