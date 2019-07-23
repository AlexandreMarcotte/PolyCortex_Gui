from collections import deque
#--My Packages--
from ..pipeline_stage import PipelineStage
from .filter import Filter
from typing import Dict
from V2.pipeline.signal_streamer.signal_collector import SignalCollector


class FilterStage(PipelineStage):
    def __init__(self,
                 queue_len,
                 filters):
        """filter : A list of filter"""

        super().__init__(queue_len)

        # self.signal_collector = signal_collector
        self.filters: Dict[str: Filter] = filters

        self.n_ch = 8

        # Variables to filter signal by chunks
        self.total_data_created = 0
        self.filter_itt = 0
        self.filter_once_every = 20 # there is a shift happening if this number is too low
        self.filter_chunks = [deque([]) for _ in range(self.n_ch)]
        self.filtered_data = [deque([]) for _ in range(self.n_ch)]

    def work(self, input):
        # self.event.wait()

        # Warning: TODO: ALEXM: Improve
        # This value is not always 1: This means that the synchronicity of the
        # two thread (creator and filter) is not perfect
        # Find a way to improve it. Maybe by using Queue instead of deque

        # n_new_data = self.signal_collector.n_data_created - self.total_data_created

        # self.total_data_created = self.signal_collector.n_data_created

        # print('n_new_data: ', n_new_data)
        # print('total_data_created: ', self.total_data_created,
        #       'filter_itt: ', self.filter_itt)

        self.filter_itt += 1
        for ch in range(self.n_ch):
            if self.filter_itt % self.filter_once_every == 0:

                # Set the filtered data to be the input so that both filter
                # are applied on the data
                self.filtered_data[ch] = input[ch]
                for filter in self.filters.values():
                    self.filtered_data[ch] = filter.filter_signal(self.filtered_data[ch])

                # Set output as chunk
                filtered_data_chunk = self.filtered_data[ch][-self.filter_once_every:]
                self.filter_chunks[ch] = deque(filtered_data_chunk)
            try:
                self.output[ch].append(self.filter_chunks[ch].popleft())

            except IndexError:
                pass

            """
            # Set output directly and completly from the filter process
            # We can see the problem at the beginning of the filtered data 
            # in this version of the code
            try:
                for i in range(len(self.output[0])):
                    self.output[ch].append(self.filtered_data[ch][i])
            except IndexError:
                print('List is empty', self.signal_collector.n_data_created)
            """

        # self.event.clear()

