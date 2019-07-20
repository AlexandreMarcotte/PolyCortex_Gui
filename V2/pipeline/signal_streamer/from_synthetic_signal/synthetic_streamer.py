from time import sleep
from typing import List
# --My Packages--
from V2.pipeline.signal_streamer.signal_collector import SignalCollector
from ..streamer import Streamer
from time import time


class SyntheticStreamer(Streamer):
    """
    class that emulate OpenBCI interface for testing with either:
        - Synthetic data (sinus/noise/impulsion)
        - CSV data (ex: data save from OpenBCI experiment)
    # Arguments:
        signal_streamer:
        signal_collector:
        stream_freq:
    """
    def __init__(self,
                 input_signal: List[List],
                 signal_collector: SignalCollector,
                 stream_freq: int=250): # Need to stream at the length of the
        # input for the frequency to correspond with the sin frequencies
        super().__init__(input_signal, signal_collector, stream_freq)

        self.stream_signal = True

    def _stream_signal(self):
        """Loop over the array of data to send into the data collector"""
        while self.stream_signal:
            # Loop over the input signal
            for single_signal in self.input_signal:
                self.signal_collector.fill_signal_queue(
                    single_signal, timestamp=self.time_stamp())
                sleep(self.real_stream_period)

                self.adjust_stream_period()



