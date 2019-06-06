from threading import Thread
from abc import abstractclassmethod
from time import time
# --My Packages--
from V2.pipeline.generate_signal.signal_collector import SignalCollector


class Streamer(Thread):
    def __init__(self,
                 input_signal: list,
                 signal_collector: SignalCollector,
                 stream_freq: int = 1000):
        super().__init__()

        self.input_signal = input_signal
        self.signal_collector = signal_collector
        self.daemon = True

        self.stream_period = self._stream_period(stream_freq)

        self.t_init = time()
        self.start()

    def time_stamp(self):
        """Calculate time elapse since beginning of the thread"""
        return time() - self.t_init

    def _stream_period(self, stream_freq):
        """Calculate period from frequency"""
        return 1 / stream_freq

    def run(self):
        """Start the creation of the thread that create signal"""
        self.stream_signal()

    @abstractclassmethod
    def stream_signal(cls):
        """Overload this function to loop over the array of data to send into
           the data collector"""

    @abstractclassmethod
    def work(self, single_signal):
        """Override this function to fill the signal queue of the data
            collector with every new signal that is received"""

