from threading import Event
# --My Packages--
from ..pipeline.signal_streamer.signal_collector import SignalCollector
# from ..pipeline.signal_streamer.from_open_bci.from_open_bci import SampleDataFromOpenBci
from .pipeline_stages.fft_stage.fft_stage import FftStage
from ..pipeline.pipeline_stages.filter_stage.filter_stage import FilterStage
from V2.pipeline.pipeline_stages.filter_stage.filter import Filter
from .signal_streamer.signal_streamer_selector import SignalStreamerSelector


class Pipeline:
    def __init__(self):
        super().__init__()
        event = Event()

        self.QUEUE_LEN = 1500

        # Filter stage
        self.filter_stage = FilterStage(
            filters={
                'bandpass':
                     Filter(cut_freq=(1, 116), filter_type='bandpass'),
                'bandstop':
                    Filter(cut_freq=(55, 65), filter_type='bandstop')
            }, event=event, queue_len=self.QUEUE_LEN)

        self.signal_collector = SignalCollector(
            len=self.QUEUE_LEN, event=event, filter_stage=self.filter_stage)

        # Streamer
        self.streamer = SignalStreamerSelector(
            stream_origin='File',  #'Synthetic data',
            signal_collector=self.signal_collector).streamer

        # FFT stage
        self.fft_stage = FftStage(
            # input=self.signal_collector.input,
            input=self.filter_stage.output,
            timestamps=self.signal_collector.timestamps, remove_first_freq=1)

    def start(self):
        self.streamer.start()
        # self.filter_stage.start()
        self.fft_stage.start()


