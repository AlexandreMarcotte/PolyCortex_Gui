from time import time, sleep
import threading
from V2.pipeline.general_func.time_this import time_this
from V2.pipeline.input_signal.sinus_signal import SinusSignal
# --My Packages--
from V2.GUI.basic_scroll_plot import BasicScrollPlot


class SignalStreamer(threading.Thread):
    """
    class that emulate OpenBCI interface for testing with either:
        - Synthetic data
        - File data
    # Arguments:
        input_signal:
        signal_collector:
        stream_freq:
    """
    def __init__(self, input_signal, signal_collector, stream_freq=100):
        super().__init__()

        self.input_signal = input_signal
        self.signal_collector = signal_collector

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
        t_init = time()
        while True:
            # Loop over the input signal
            for single_signal in self.input_signal:
                # Fill the signal queue with the data collector
                self.signal_collector.fill_signal_queue(
                        single_signal, timestamp=self.time_stamp(t_init))
                sleep(self.stream_period)


if __name__ == '__main__':
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtGui
    win = pg.GraphicsWindow()

    from V2.pipeline.signal_collector import SignalCollector
    sinus_signal = SinusSignal()
    signal_collector = SignalCollector()
    signal_streamer = SignalStreamer(
            input_signal=sinus_signal.array,
            signal_collector=signal_collector)
    signal_streamer.start()

    v1 = BasicScrollPlot(
            win, pos=(0, 0), display_queue=signal_collector.signal_deque)
    v1.timer.start(10)
    QtGui.QApplication.instance().exec_()



