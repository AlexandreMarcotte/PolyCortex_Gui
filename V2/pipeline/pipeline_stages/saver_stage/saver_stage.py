import numpy as np
from collections import deque
# --My Packages--
from V2.pipeline.pipeline_stages.pipeline_stage import PipelineStage


class saver_stage(PipelineStage):
    def __init__(self, save_path, input, timestamps, stream_period):
        super().__init__(input, stream_period=stream_period)

        self.save_path = save_path
        self.save_signal = deque()

    def run(self):
        while self.run_stage:
            self.save_signal
            self.work()

    def work(self):
        with open(self.save_path, 'a') as f:
            np.savetxt(f, self.output, delimiter=',')
