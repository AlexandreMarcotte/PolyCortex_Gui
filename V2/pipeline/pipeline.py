from threading import Event
# --My Packages--
from ..pipeline.signal_streamer.signal_collector.signal_collector import SignalCollector
# from ..pipeline.signal_streamer.from_open_bci.from_open_bci import SampleDataFromOpenBci
from .pipeline_stages.fft_stage.fft_stage import FftStage
from ..pipeline.pipeline_stages.filter_stage.filter_stage import FilterStage
from V2.pipeline.pipeline_stages.filter_stage.filter import Filter
from .signal_streamer.signal_streamer_selector import SignalStreamerSelector
from V2.general_settings import GeneralSettings


class Pipeline:
    def __init__(self, stream_origin='File'):
        super().__init__()

        self.QUEUE_LEN = GeneralSettings.QUEUE_LEN
        self.N_CH = GeneralSettings.N_CH

        # Filter stage
        self.filter_stage = FilterStage(
            filters={
                'bandpass': [Filter(cut_freq=(2, 116), type='bandpass')],
                'bandstop': [Filter(cut_freq=(55, 65), type='bandstop'),
                             Filter(cut_freq=(10, 25), type='bandstop')]

            }, queue_len=self.QUEUE_LEN)

        self.signal_collector = SignalCollector(
            len=self.QUEUE_LEN, filter_stage=self.filter_stage)

        self.update_streamer(stream_origin)

        # FFT stage
        self.fft_stage = FftStage(
            # input=self.signal_collector.input,
            input=self.filter_stage.output,
            timestamps=self.signal_collector.timestamps, remove_first_freq=1,
            n_ch=self.N_CH)

    def update_streamer(self, stream_origin):
        # Streamer
        self.streamer = SignalStreamerSelector(
            stream_origin=stream_origin,
            signal_collector=self.signal_collector).streamer

    def start(self):
        self.streamer.start()
        # self.filter_stage.start()
        self.fft_stage.start()


