from V2.pipeline.pipeline_stages.pipeline_stage import PipelineStage
from V2.pipeline.pipeline_stages.filter_stage.filter import Filter


class FilterStage(PipelineStage):
    def __init__(self, input):
        """filter : A list of filter"""
        super().__init__(input)
        self.filter = Filter()
        self.start()

    def work(self):
        filtered_data = self.filter.filter_signal(self.input)
        # Set all the data to the output
        for i in range(len(self.output)):
            self.output[i] = filtered_data[i]
