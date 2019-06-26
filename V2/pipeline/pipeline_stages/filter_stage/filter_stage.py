from V2.pipeline.pipeline_stages.pipeline_stage import PipelineStage


class FilterStage(PipelineStage):
    def __init__(self, input: list, filter: list):
        """filter : A list of filter"""
        super().__init__(input)
        self.filter = filter

    def work(self):
        for ch in range(len(self.input)):
            # print('filter_stage: Work')
            filtered_data = self.input[ch]
            for filter in self.filter:
                filtered_data = filter.filter_signal(filtered_data)
            # Set all the data to the output
            for i in range(len(self.output[ch])):  # TODO: ALEXM Find a better way to do this  (make a copy ?)
                self.output[ch][i] = filtered_data[i]

