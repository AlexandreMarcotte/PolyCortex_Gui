from ..pipeline_stage import PipelineStage
from .filter import Filter
from typing import Dict, List


class FilterStage(PipelineStage):
    def __init__(self,
                 input: List,
                 filters):
        """filter : A list of filter"""
        super().__init__(input)
        self.input = input
        self.filters: Dict[str: Filter] = filters

    def work(self):
        for ch in range(len(self.input)):
            filtered_data = self.input[ch]
            for filter in self.filters.values():
                filtered_data = filter.filter_signal(filtered_data)
            # Set all the data to the output
            for i in range(len(self.output[ch])):  # TODO: ALEXM Find a better way to do this  (make a copy ?)
                self.output[ch][i] = filtered_data[i]

