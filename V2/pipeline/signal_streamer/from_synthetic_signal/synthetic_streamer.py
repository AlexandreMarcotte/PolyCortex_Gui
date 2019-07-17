from time import sleep
# --My Packages--
from V2.pipeline.signal_streamer.signal_collector import SignalCollector
from ..streamer import Streamer


class SyntheticStreamer(Streamer):
    """
    class that emulate OpenBCI interface for testing with either:
        - Synthetic data (sinus/noise/impulsion)
        - CSV data (ex: data savec from OpenBCI experiment)
    # Arguments:
        signal_streamer:
        signal_collector:
        stream_freq:
    """
    def __init__(self,
                 input_signal: list,
                 signal_collector: SignalCollector,
                 stream_freq: int = 1000):
        super().__init__(input_signal, signal_collector, stream_freq)
        self.stream_signal = True

    def stream_signal(self):
        """Loop over the array of data to send into the data collector"""
        while self.stream_signal:
            # Loop over the input signal
            for single_signal in self.input_signal:
                self.signal_collector.fill_signal_queue(
                    single_signal, timestamp=self.time_stamp())
                sleep(self.stream_period)

