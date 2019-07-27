# --General Packages--
import numpy as np
from collections import deque
from PyQt5.QtCore import pyqtSignal, QObject
# -- My Packages --
from V2.general_settings import GeneralSettings
from V2.pipeline.pipeline_stages.filter_stage.filter_stage import FilterStage
from .signal_long_term_memory import SignalLongTermMemory


class SignalCollector(QObject):

    filled_new_data_into_queue = pyqtSignal()

    def __init__(self, len=GeneralSettings.QUEUE_LEN, use_reader=False,
                 filter_stage:FilterStage=None):
        super().__init__()

        self.filter_stage = filter_stage
        self.long_term_memory = SignalLongTermMemory()

        self.n_data_created = 0
        self.input = [deque(np.zeros(len), maxlen=len)
                      for _ in range(GeneralSettings.N_CH)]
        self.timestamps = deque(np.zeros(len), maxlen=len)
        self.experiments = deque(np.zeros(len), maxlen=len)
        self.experiment_event = 0
        self.events_pos = []
        # Reader
        self.use_reader = use_reader
        self.reader_queue = deque(np.zeros(len))

    def fill_signal_queue(self, signal, timestamp=None):
        """Fill the signal queue with one new signal and its corresponding
        timestamp"""
        self.experiments.append(self.experiment_event)

        self.n_data_created += 1
        for ch, val in enumerate(signal):
            self.input[ch].append(val)

        # Filter data
        self.filter_stage.work(self.input)
        # long term memory
        self.long_term_memory.store_long_term_memory(
            signal, timestamp, self.experiment_event)
        # Remove the event
        if self.experiment_event:
            # put a signal here !!!
            self.experiment_event = 0
            # add the position of the current event that was detected
            self.events_pos.append(0)
            print(self.events_pos)

        # Update the pos to show the position of the regions event
        for i in range(len(self.events_pos)):
            self.events_pos[i] += 1

        if self.events_pos:
            if self.events_pos[0] > GeneralSettings.QUEUE_LEN-10:
                del self.events_pos[0]
        self.timestamps.append(timestamp)


