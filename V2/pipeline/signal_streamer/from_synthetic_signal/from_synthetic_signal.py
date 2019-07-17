import numpy as np
# --My Packages--
from V2.pipeline.signal_streamer.from_synthetic_signal.sinus_signal import SinusSignal


class SyntheticSignal:
    def __init__(self):
        self.signal = self.create_synthetic_signal()

    def create_synthetic_signal(self):
        sinus_signal = (SinusSignal(2, 60).array
                      + SinusSignal(1, 4).array
                      + SinusSignal(3, 10).array)
                      # + SinusSignal(3, 90).array)

        sinus_signal = self.add_impulsion(sinus_signal)
        # sinus_signal += np.random.random(len(sinus_signal)) * 6

        return sinus_signal

    def create_sum_of_sin_signals(self, sinus_signals: list):
        return sum([SinusSignal(amplitude, angular_freq).array for
                         amplitude, angular_freq in sinus_signals])

    def add_impulsion(self, signal):
        # add impulsion to sinus
        for i in range(len(signal)):
            if i % 200 == 0:
                signal[i] = 10
        return signal
