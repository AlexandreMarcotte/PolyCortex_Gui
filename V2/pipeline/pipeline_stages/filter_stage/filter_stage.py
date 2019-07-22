from collections import deque
#--My Packages--
from ..pipeline_stage import PipelineStage
from .filter import Filter
from typing import Dict
from V2.pipeline.signal_streamer.signal_collector import SignalCollector

class FilterStage(PipelineStage):
    def __init__(self,
                 signal_collector: SignalCollector,
                 filters,
                 event=None):
        """filter : A list of filter"""

        super().__init__(len(signal_collector.input[0]), stream_period=0.01)

        self.signal_collector = signal_collector
        self.filters: Dict[str: Filter] = filters
        self.event = event

        self.n_ch = len(self.signal_collector.input)

        # Variables to filter signal by chunks
        self.total_data_created = 0
        self.filter_itt = 0
        self.filter_once_every = 10
        self.filter_chunks = [deque([]) for _ in range(self.n_ch)]
        self.filtered_data = [deque([]) for _ in range(self.n_ch)]

    def work(self):
        self.event.wait()
        # Warning: TODO: ALEXM: Improve
        # This value is not always 1: This means that the synchronicity of the
        # two thread (creator and filter) is not perfect
        # Find a way to improve it. Maybe by using Queue instead of deque
        n_new_data = self.signal_collector.n_data_created - self.total_data_created

        self.filter_itt += 1
        for ch in range(self.n_ch):
            if self.filter_itt % self.filter_once_every == 0:
                # Set the filtered data to be the input so that both filter
                # are applied on the data
                self.filtered_data[ch] = self.signal_collector.input[ch]
                for filter in self.filters.values():
                    filtered_data = filter.filter_signal(self.filtered_data[ch])
                    filtered_data_chunk = filtered_data[-self.filter_once_every:]
                    self.filter_chunks[ch] = deque(filtered_data_chunk)
            try:
                self.output[ch].append(self.filter_chunks[ch].popleft())
            except IndexError:
                print('List is empty', self.signal_collector.n_data_created)

        self.event.clear()

