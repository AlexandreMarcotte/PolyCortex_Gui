from V2.pipeline.generate_signal.from_synthetic_signal.sinus_signal import SinusSignal


class SyntheticSignal:
    def __init__(self):
        self.signal = self.create_synthetic_signal()

    def create_synthetic_signal(self):
        sin1 = SinusSignal(amplitude=2, angular_freq=60, len=1000)
        sin2 = SinusSignal(amplitude=1, angular_freq=4, len=1000)

        synthetic_signal = sin1.array + sin2.array

        synthetic_signal = self.add_impulsion(synthetic_signal)

        return synthetic_signal

    def add_impulsion(self, signal):
        # add impulsion to sinus
        for i in range(len(signal)):
            if i % 200 == 0:
                signal[i] = 10
        return signal
