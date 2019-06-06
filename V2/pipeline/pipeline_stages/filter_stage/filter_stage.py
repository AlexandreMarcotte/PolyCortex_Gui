from V2.pipeline.pipeline_stages.pipeline_stage import PipelineStage


class FilterStage(PipelineStage):
    def __init__(self, input, filter: list):
        """filter : A list of filter"""
        super().__init__(input)
        self.filter = filter

    def work(self):
        print('filter_stage: Work')
        filtered_data = self.input
        for f in self.filter:
            filtered_data = f.filter_signal(filtered_data)
        # Set all the data to the output
        for i in range(len(self.output)):  # TODO: ALEXM Find a better way to do this
            self.output[i] = filtered_data[i]

