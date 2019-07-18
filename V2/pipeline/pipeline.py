from ..pipeline.signal_streamer.signal_collector import SignalCollector
# from ..pipeline.signal_streamer.from_open_bci.from_open_bci import SampleDataFromOpenBci
from .pipeline_stages.fft_stage.fft_stage import FftStage
from ..pipeline.pipeline_stages.filter_stage.filter_stage import FilterStage
from V2.pipeline.pipeline_stages.filter_stage.filter import Filter
from .signal_streamer.signal_streamer_selector import SignalStreamerSelector


class Pipeline:
    def __init__(self):
        self.signal_collector = SignalCollector(len=1000)
        # self.streamer = self.start_signal_streamer(stream_origin='File')
        self.streamer = SignalStreamerSelector(
            stream_origin='File',
            signal_collector=self.signal_collector).streamer
        # self.streamer.start()
        # Filter
        self.filter_stage = FilterStage(
                input=self.signal_collector.input,
                filter=[Filter(cut_freq=(92,), filter_type='low'),
                        Filter(cut_freq=(1, 15), filter_type='bandstop')])
        self.filter_stage.start()
        # FFT
        self.fft_stage = FftStage(
            input=self.signal_collector.input,
            timestamps=self.signal_collector.timestamps, remove_first_freq=1)

    def start(self):
        self.streamer.start()
        self.fft_stage.start()


