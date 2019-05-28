from threading import Thread
from collections import deque
from abc import abstractclassmethod
import time


class PipelineStage(Thread):
    def __init__(self, input):
        super().__init__()
        self.input = input

        self.output = deque(input, maxlen=len(input))

        self.daemon = True

    def run(self):
        while True:
            self.work()
            time.sleep(0.04)  # instead to it every time there is N new value

    @abstractclassmethod
    def work(self):
        """Override this method to create a stage"""
        return

    def show_signal(self):
        """Show signal in individual window to for testing purpose"""
        pass

