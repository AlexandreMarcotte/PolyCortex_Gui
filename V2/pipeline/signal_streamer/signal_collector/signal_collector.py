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
        self.experiment_type = deque(np.zeros(len))
        # Reader
        self.use_reader = use_reader
        self.reader_queue = deque(np.zeros(len))

    def fill_signal_queue(self, signal, timestamp=None):
        """Fill the signal queue with one new signal and its corresponding
        timestamp"""

        self.n_data_created += 1
        for ch, val in enumerate(signal):
            self.input[ch].append(val)

        # Filter data
        self.filter_stage.work(self.input)
        # long term memory
        self.long_term_memory.store_long_term_memory(signal, timestamp)

        self.timestamps.append(timestamp)


