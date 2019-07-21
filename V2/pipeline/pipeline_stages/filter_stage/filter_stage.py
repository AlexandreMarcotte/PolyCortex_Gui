import numpy as np
from collections import deque
#--My Packages--
from ..pipeline_stage import PipelineStage
from .filter import Filter
from typing import Dict, List
# from ..pipeline.signal_streamer.signal_collector import SignalCollector


class FilterStage(PipelineStage):
    def __init__(self,
                 signal_collector,
                 filters,
                 event=None):
        """filter : A list of filter"""
        super().__init__(len(signal_collector.input[0]), stream_period=0.01)
        # self.input = input
        # self.input = signal_collector.input
        self.signal_collector = signal_collector
        self.filters: Dict[str: Filter] = filters
        self.event = event

        self.n_ch = len(self.signal_collector.input)
        # Variables to filter signal by chunks
        self.filter_itt = 0
        self.total_data_created = 0
        self.TEST_TOTAL = 0
        self.filter_once_every = 5
        self.filter_chunks = [[] for _ in range(self.n_ch)]
        # Remove average
        self.averages = np.zeros(self.n_ch)
        self.filtered_data = [deque([]) for _ in range(self.n_ch)]

    def work(self):
        self.event.wait()

        # Warning
        # This value is not always 1: This means that the synchronicity of the
        # two thread (creator and filter) is not perfect
        # Find a way to improve it. Maybe by using Queue instead of deque
        n_new_data = self.signal_collector.n_data_created - self.total_data_created

        # self.total_data_created = self.signal_collector.n_data_created
        # self.TEST_TOTAL += n_new_data
        # print('new data', n_new_data)
        # print('N_data_created', self.signal_collector.n_data_created)
        # print('TEST TOTAL ', self.TEST_TOTAL)
        self.filter_itt += 1
        # if self.filter_itt % self.filter_once_every == 0:
            # print('-----------------')
        for ch in range(self.n_ch):

            if self.filter_itt % self.filter_once_every == 0:  # THIS DOESTN WORK BECAUSE FILTER ITT HAPPEN LESS REGULARILY THAN THE ACQUISITION OF THE DATA
                # HOW TO PUT TWO THREAD ONE AFTER THE OTHER
                # YOU CAN SEE THE PROBLEM FROM THE LONG LINE IT ALMOST WORK SEEMLESSLY IF I PUT A TIMES THREE VALUE IN THE [_SELF"FILTER-ONCE-EVERY] BRAQUET

                # Set the filtered data to be the input so that both filter
                # are applied on the data
                self.filtered_data[ch] = self.signal_collector.input[ch]
                for filter in self.filters.values():
                    filtered_data = filter.filter_signal(self.filtered_data[ch])
                    filtered_data_chunk = filtered_data[-self.filter_once_every:]
                    self.filtered_data[ch] = deque(filtered_data_chunk)

            try:
                self.output[ch].append(self.filtered_data[ch].popleft())
                # print(len(self.filtered_data[ch]))
                # for _ in range(n_new_data):
                #     self.output[ch].append(self.filtered_data[ch].popleft())
                # for i in range(len(self.output[ch])):
                #     self.output[ch][i] = self.filtered_data[ch][i]  # - self.averages[ch]
            except IndexError:
                print('List is empty')
                print(self.signal_collector.n_data_created)
            #     print(self.filter_itt)
                    # TODO: instead filter in chunk and append where there is a signal emited from the signal collector
                    # self.filtered_data[:70] = 0
        self.event.clear()

        """
                for i in range(len(self.output[ch])):
                    # Remove the mean of the signal
                    self.output[ch][i] = self.filtered_data[i]  # - self.averages[ch]
        """
        """
                    # keep only the last value of the filter process
                    self.filter_chunks[ch] = list(
                        filtered_data[-self.filter_once_every:])
        # put the data once at the time at every loop so the signal is not showing
        # all jerky
        if any(self.filter_chunks[0]):
            for ch in range(self.n_ch):
            # empty one value in the filter_chunk
                val = self.filter_chunks[ch].pop()
                self.output[ch].append(val)
        # print(len(self.filter_chunks[0]))

                # Set all the data to the output
                # for i in range(len(self.output[ch])):  # TODO: ALEXM Find a better way to do this  (make a copy ?)
                #     self.output[ch][i] = filtered_data[i]

        """
