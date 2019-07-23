# --My packages--
from V2.pipeline.pipeline import Pipeline


class Model:
    def __init__(self):
        self.N_CH = 8

        self.pipeline = Pipeline()

        self.board = None

    def update_pipeline(self, stream_origin):
        print('set stream origin', stream_origin)
        self.pipeline = Pipeline(stream_origin)
