# --General Packages--
import numpy as np
from collections import deque
# --My Packages--
from V2.pipeline.pipeline_stages.pipeline_stage import PipelineStage
from .freq_band_over_time import FreqBandOverTime
from V2.utils.waves import waves


class FftStage(PipelineStage):
    def __init__(self, input, timestamps, remove_first_freq=1, n_ch=8):
        super().__init__(len(input[0]), stream_period=0.2)

        self._n_ch = n_ch
        # The output needs to be half the length because of the fft
        self.output = [deque(input[0], maxlen=len(input[0])//2)
                       for _ in range(len(input))]
        self.input = input
        self.timestamps = timestamps
        # self.remove_first_freq = remove_first_freq

        self.freq_range = np.ones(len(input[0])//2)

        self.N_T_MEMORY = 200
        self.fft_over_time = [
            deque(maxlen=self.N_T_MEMORY) for _ in range(n_ch)]

        # -------- Power band ---------
        self.freq_per_band_all_ch = [None for _ in range(n_ch)]
        self.slices = None
        self._set_waves(waves)

    def work(self):
        self.freq_range = self._get_freq_range(len(self.input[0]))
        for ch, input in enumerate(self.input):
            self.output[ch] = self._calcul_fft(input)
            # keep track of fft values over time
            self.fft_over_time[ch].append(self.output[ch])
            self.freq_per_band_all_ch[ch] = self.get_avg_freq_per_band(ch)
            print('------------------')
            print(self.freq_per_band_all_ch[ch])
            print('------------------')

    def _calcul_fft(self, queue):
        fft = np.fft.fft(queue)
        # Take the abs value to be in the Reel domain
        output = abs(fft[:len(queue)//2])
        return output

    def _get_freq_range(self, n_data):
        """Calculate FFT (Remove freq 0 because it gives a really high
         value on the graph"""
        # Remove the opposite side of the fft which is a symmetry
        freq_range = np.linspace(0, n_data//2/self._get_delta_t(), n_data//2)
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
            FreqBandOverTime(len(self.waves.values()), self.N_T_MEMORY)
            for _ in range(self._n_ch)]

    def set_slice_for_all_waves(self):
        self.slices = [
            slice(w.freq_range[0], w.freq_range[1])
            for w in self.waves.values()]

    def get_avg_freq_per_band(self, ch):
        freq_per_band = [np.average(self.output[ch][s]) for s in self.slices]
        # for ch, f in enumerate(freq_per_band):
        # for ch in range(len(self.all_freq_band_over_time)):
        self.all_freq_band_over_time[ch].add_data_to_queue(freq_per_band)
        return freq_per_band



