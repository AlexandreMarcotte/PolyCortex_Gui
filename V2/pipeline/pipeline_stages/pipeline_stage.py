from threading import Thread
from collections import deque
from abc import abstractclassmethod
import time
import numpy as np


class PipelineStage(Thread):
    def __init__(self, signal_len, stream_period=0.01):
        super().__init__()
        self.output = [deque(np.zeros(signal_len), maxlen=signal_len)
                       for _ in range(8)]

        self.daemon = True
        self.run_stage = True
        self.stream_period = stream_period

    def run(self):
        while self.run_stage:
            self.work()
            time.sleep(self.stream_period)  # instead to it every time there is N new value

    @abstractclassmethod
    def work(self):
        """Override this method to create a stage"""
        return

    # def show_signal(self):
    #     """Show signal in individual window to for testing purpose"""
    #     pass

