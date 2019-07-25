from threading import Thread
from abc import abstractclassmethod
from time import time, sleep
# --My Packages--
from V2.pipeline.signal_streamer.signal_collector.signal_collector import SignalCollector
from .stream_frequency_adjustor import StreamFrequencyAdjustor


class Streamer(Thread):
    def __init__(self,
                 input_signal: list,
                 signal_collector: SignalCollector,
                 stream_freq: int = 1000):
        super().__init__()

        self.input_signal = input_signal
        self.signal_collector = signal_collector
        self.daemon = True

        self.desired_stream_period = self._stream_period(stream_freq)

        self.real_stream_period = self.desired_stream_period
        self.stream_freq_adjustor = StreamFrequencyAdjustor(
            desired_stream_period=self.desired_stream_period)

        self.t_init = time()

    def time_stamp(self):
        """Calculate time elapse since beginning of the thread"""
        return time() - self.t_init

    def _stream_period(self, stream_freq):
        """Calculate period from frequency"""
        return 1 / stream_freq

    def adjusted_sleep(self):
        # TODO: ALEXM: Don't call at every iterations ??
        self.real_stream_period = \
            self.stream_freq_adjustor.adjust_real_stream_period(
                current_t_stamp=time(),
                real_stream_period=self.real_stream_period)
        sleep(self.real_stream_period)

    def run(self):
        """Start the creation of the thread that create signal"""
        self._stream_signal()

    @abstractclassmethod
    def _stream_signal(self):
        """Overload this function to loop over the array of data to send into
           the data collector"""

    # @abstractclassmethod
    # def work(self, single_signal):
    #     """Override this function to fill the signal queue of the data
    #         collector with every new signal that is received"""


