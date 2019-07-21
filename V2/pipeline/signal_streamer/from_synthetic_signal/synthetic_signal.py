import numpy as np
# --My Packages--
from ..from_synthetic_signal.sinus_signal import SinusSignal


class SyntheticSignal:
    def __init__(self, n_ch=8, do_add_impulsion=False, do_add_random_noise=False,
                 do_add_sum_of_sin=True):
        self.n_ch = n_ch
        self.do_add_impulsion = do_add_impulsion
        self.do_add_random_noise = do_add_random_noise
        self.do_add_sum_of_sin = do_add_sum_of_sin

        self.SIGNAL_LEN = 250

        # self.signal = self._create_synthetic_signal()
        self.signal = self._create_signal_to_test_filters()

        self.signals = self.duplicate_signal_over_many_ch()

    def _create_synthetic_signal(self):
        sinus_signal = (SinusSignal(0.1, 4).array
                      + SinusSignal(2, 10).array
                      + SinusSignal(8, 60).array)

        if self.do_add_random_noise:
            sinus_signal += self._random_noise_signal(sinus_signal)

        if self.do_add_sum_of_sin:
            sinus_signal += self._sum_of_sin_signals(1, 100)

        if self.do_add_impulsion:
            sinus_signal = self._add_impulsion_to_signal(sinus_signal)

        return sinus_signal

    def _create_signal_to_test_filters(self):
        return self._sum_of_sin_signals(1, 100) + 100

    def _sum_of_sin_signals(self, start, stop):
        return sum(SinusSignal(4, freq).array for freq in range(start, stop))

    def _random_noise_signal(self, sinus_signal):
        return np.random.random(len(sinus_signal)) * 6

    def _add_impulsion_to_signal(self, signal):
        # add impulsion to sinus
        for i in range(len(signal)):
            if i % 200 == 0:
                signal[i] = 10
        return signal

    def duplicate_signal_over_many_ch(self):
        signals = [[val]*self.n_ch for val in self.signal]
        return signals

    # def create_sum_of_sin_signals(self, sinus_signals: list):
    #     return sum([SinusSignal(amplitude, angular_freq).array for
    #                      amplitude, angular_freq in sinus_signals])

