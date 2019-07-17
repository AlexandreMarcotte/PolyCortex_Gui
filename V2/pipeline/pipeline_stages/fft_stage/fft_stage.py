import numpy as np
from collections import deque
from V2.pipeline.pipeline_stages.pipeline_stage import PipelineStage


class FftStage(PipelineStage):
    def __init__(self, input, timestamps, remove_first_freq=1):
        super().__init__(input)
        # The output needs to be half the length because of the fft
        self.output = [deque(input[0], maxlen=len(input[0])//2)
                       for _ in range(len(input))]
        self.input = input
        self.timestamps = timestamps
        self.remove_first_freq = remove_first_freq

        self.freq_range = np.ones(len(input[0])//2)

    def work(self):
        for ch, input in enumerate(self.input):
            self.freq_range, self.output[ch] = self._get_fft_to_plot(input)

    def _get_fft_to_plot(self, queue):
        fft = self._calcul_fft(queue)
        freq_range = self._get_freq_range(len(queue))
        return freq_range, fft

    def _calcul_fft(self, queue):
        fft = np.fft.fft(queue)
        output = abs(fft[:len(queue) // 2])
        return output

    def _get_freq_range(self, n_data):
        """Calculate FFT (Remove freq 0 because it gives a really high
         value on the graph"""
        freq_range = np.linspace(0, n_data//2/self._get_delta_t(), n_data//2)
        return freq_range

    def _get_delta_t(self):
        """interval of time from the first to the last value that was
        add to the queue"""
        return self.timestamps[-1] - self.timestamps[0]





        # self.gv = gv
        # self.remove_first_data = remove_first_data

        # self.freq_per_band_all_ch = [None for _ in range(self.gv.N_CH)]
        # self.activated = False
        # self.freq_range = 100
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.calcul_frequency)
        # self.fft = [None for _ in range(gv.N_CH)]
        # self.waves = None
        # self.slices = None
        # self.N_T_MEMORY = 200
        # I could also just have one deque containing list of all the time
        # stamp each list would contain the 8 values, one for every ch at
        # that time stamp
        # self.fft_over_time = [
        #     deque(maxlen=self.N_T_MEMORY) for _ in range(self.gv.N_CH)]
        # TODO: ALEXM: Filter instead of removing them direcly like that
    # def set_waves(self, waves):
    #     self.waves = waves
    #     self.set_slice_for_all_waves()
    #     self.all_freq_band_over_time = [
    #         FreqBandOverTime(len(self.waves.values()), self.N_T_MEMORY)
    #         for _ in range(self.gv.N_CH)]
    # def set_slice_for_all_waves(self):
    #     self.slices = [
    #         slice(w.freq_range[0], w.freq_range[1])
    #         for w in self.waves.values()]

    # def calcul_frequency(self):
    #     for ch in range(self.gv.N_CH):
    #         self.N_DATA = len(self.gv.data_queue[ch])
    #         self.freq_range = self.get_freq_range(self.gv.DEQUE_LEN)
    #         self.fft[ch] = self.calcul_fft(self.gv.data_queue[ch])
    #         self.fft_over_time[ch].append(self.fft[ch])
    #         self.freq_per_band_all_ch[ch] = self.get_avg_freq_per_band(ch)
    #
    # def get_avg_freq_per_band(self, ch):
    #     freq_per_band = [np.average(self.fft[ch][s]) for s in self.slices]
        # for ch, f in enumerate(freq_per_band):
        # for ch in range(len(self.all_freq_band_over_time)):
        # self.all_freq_band_over_time[ch].add_data_to_queue(freq_per_band)
        # return freq_per_band


# class FreqBandOverTime:
#     def __init__(self, N_WAVE_TYPE, N_T_MEMORY):
#         self.wave_type_data = [
#             deque(maxlen=N_T_MEMORY) for _ in range(N_WAVE_TYPE)]
#
#     def add_data_to_queue(self, waves_avg):
#         for i, val in enumerate(waves_avg):
#             self.wave_type_data[i].append(val)



