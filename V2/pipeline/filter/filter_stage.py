from V2.pipeline.pipeline_stage import PipelineStage


class FilterStage(PipelineStage):
    def __init__(self, input, filter):
        """filter : A list of filter"""
        super().__init__(input)
        self.filter = filter

    def work(self):
        filtered_data = self.filter.filter_signal(self.input)
        # Set all the data to the output
        # self.output = filtered_data
        for i in range(len(self.output)):
            self.output[i] = filtered_data[i]
