from threading import Event
# --My Packages--
from ..pipeline.signal_streamer.signal_collector import SignalCollector
# from ..pipeline.signal_streamer.from_open_bci.from_open_bci import SampleDataFromOpenBci
from .pipeline_stages.fft_stage.fft_stage import FftStage
from ..pipeline.pipeline_stages.filter_stage.filter_stage import FilterStage
from V2.pipeline.pipeline_stages.filter_stage.filter import Filter
from .signal_streamer.signal_streamer_selector import SignalStreamerSelector


class Pipeline:
    def __init__(self, stream_origin='Synthetic data'):
        super().__init__()

        self.QUEUE_LEN = 1500
        self.N_CH = 8
        self.stream_origin = stream_origin

        # Filter stage
        self.filter_stage = FilterStage(
            filters={
                # 'bandpass':
                #      Filter(cut_freq=(2, 116), filter_type='bandpass'),
                'bandstop':
                    Filter(cut_freq=(55, 65), filter_type='bandstop')
            }, queue_len=self.QUEUE_LEN)

        self.signal_collector = SignalCollector(
            len=self.QUEUE_LEN, filter_stage=self.filter_stage)

        # Streamer
        self.streamer = SignalStreamerSelector(
            stream_origin=self.stream_origin,
            signal_collector=self.signal_collector).streamer

        # FFT stage
        self.fft_stage = FftStage(
            # input=self.signal_collector.input,
            input=self.filter_stage.output,
            timestamps=self.signal_collector.timestamps, remove_first_freq=1,
            n_ch=self.N_CH)

    def start(self):
        self.streamer.start()
        # self.filter_stage.start()
        self.fft_stage.start()


