from time import time, sleep
import threading
# --My Packages--
from V2.pipeline.general_func.time_this import time_this
from V2.pipeline.signal_collector import SignalCollector


class SignalStreamer(threading.Thread):
    """
    class that emulate OpenBCI interface for testing with either:
        - Synthetic data (sinus/noise/impulsion)
        - CSV data (ex: data savec from OpenBCI experiment)
    # Arguments:
        input_signal:
        signal_collector:
        stream_freq:
    """
    def __init__(self,
                 input_signal: list,
                 signal_collector: SignalCollector,
                 stream_freq: int = 1000):
        super().__init__()

        self.input_signal = input_signal
        self.signal_collector = signal_collector
        self.daemon = True

        self.stream_period = self.stream_period(stream_freq)

    @staticmethod
    def stream_period(stream_freq):
        """Calculate period from frequency"""
        return 1 / stream_freq

    @staticmethod
    def time_stamp(t_init):
        """Calculate time elapse since beginning of the thread"""
        return time() - t_init

    def run(self):
        """Start the creation of the thread that create signal"""
        self.stream_signal()

    def stream_signal(self):
        """Loop over the array of data to send into the data collector"""
        t_init = time()
        while True:
            # Loop over the input signal
            for single_signal in self.input_signal:
                work_time = self.work(t_init, single_signal)
                sleep_time = self.work_sleep_proportion(work_time)
                sleep(sleep_time)

    @time_this
    def work(self, t_init, single_signal):
        """Fill the signal queue of the data collector with every new signal
            that is received"""
        self.signal_collector.fill_signal_queue(
            single_signal, timestamp=self.time_stamp(t_init))

    def work_sleep_proportion(self, work_time):
        """Calculate the sleep time based on the work time"""  # TODO: ALEXM Go back to the old way of doing it
        sleep_time = self.stream_period - work_time
        if sleep_time < 0:
            sleep_time = 0
            print('works take longer that period time')
        return sleep_time

