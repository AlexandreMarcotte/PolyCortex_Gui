# --My Packages--
from ..from_synthetic_signal.sinus_signal import SinusSignal


class SyntheticSignal:
    def __init__(self, n_ch=8, do_add_impulsion=False):
        self.n_ch = n_ch
        self.do_add_impulsion = do_add_impulsion

        self.signal = self._create_synthetic_signal()
        self.signals = self.duplicate_signal_over_many_ch()

    def _create_synthetic_signal(self):
        sinus_signal = (SinusSignal(2, 60).array
                      + SinusSignal(1, 4).array
                      + SinusSignal(1, 100).array
                      + SinusSignal(3, 10).array)
                      # + SinusSignal(3, 90).array)

        if self.do_add_impulsion:
            sinus_signal = self.add_impulsion(sinus_signal)
        # sinus_signal += np.random.random(len(sinus_signal)) * 6
        return sinus_signal

    def duplicate_signal_over_many_ch(self):
        signals = [[val]*self.n_ch for val in self.signal]
        return signals

    def add_impulsion(self, signal):
        # add impulsion to sinus
        for i in range(len(signal)):
            if i % 200 == 0:
                signal[i] = 10
        return signal

    # def create_sum_of_sin_signals(self, sinus_signals: list):
    #     return sum([SinusSignal(amplitude, angular_freq).array for
    #                      amplitude, angular_freq in sinus_signals])

