# -- General Packages --
from collections import deque
# -- My Packages --
from V2.general_settings import GeneralSettings
from V2.utils.write_to_file import append_to_file


# Could be set in memory all at once or once every number of data
class SignalLongTermMemory:
    def __init__(self, dump_every_n_values=2500):

        self.dump_every_n_values = dump_every_n_values

        self.first_save = True
        self.n_data_in_memory = 0

        self.output = [deque() for _ in range(GeneralSettings.N_CH)]
        self.timestamp = deque()
        self.experiment_type = deque()

    def store_long_term_memory(self, signal, timestamp, event):
        for ch, val in enumerate(signal):
            self.output[ch].append(val)
        self.timestamp.append(timestamp)
        self.experiment_type.append(event)

        self.n_data_in_memory += 1
        if self.n_data_in_memory > self.dump_every_n_values:
            self.dump_memory_into_file()

    def dump_memory_into_file(self):
        print('dumping memory into file')
        append_to_file(
            self.output, self.timestamp, self.experiment_type,
            self.first_save)

        self.clear_memory()

        self.first_save = False

    def clear_memory(self):
        # Dump memory
        for ch in range(GeneralSettings.N_CH):
            self.output[ch].clear()
        self.timestamp.clear()
        self.experiment_type.clear()
        self.n_data_in_memory = 0




