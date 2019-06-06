from ..pipeline.generate_signal.signal_collector import SignalCollector
from ..pipeline.generate_signal.from_synthetic_signal.synthetic_streamer import SyntheticStreamer
from ..pipeline.generate_signal.from_file.file_streamer import FileStreamer
from ..pipeline.pipeline_stages.filter_stage.filter_stage import FilterStage
from ..pipeline.generate_signal.from_synthetic_signal.from_synthetic_signal import SyntheticSignal
from .pipeline_stages.fft_stage.fft_stage import FftStage
from V2.pipeline.pipeline_stages.filter_stage.filter import Filter


class Pipeline:
    def __init__(self):
        self.start()

    def start(self):
        self.signal_collector = SignalCollector(len=1000)
        self.streamer = self.start_signal_streamer()
        # Filter
        self.filter_stage = FilterStage(
                input=self.signal_collector.input,
                filter=[#Filter(cut_freq=(92,), filter_type='low'),
                        Filter(cut_freq=(55, 65), filter_type='bandstop')])
        self.filter_stage.start()
        # FFT
        self.fft_stage = FftStage(
                input=self.filter_stage.input,
                timestamps=self.signal_collector.timestamps)
        self.fft_stage.start()

    def start_signal_streamer(self, stream_origin='Synthetic data'):

        if stream_origin == 'Synthetic data':
            streamer = SyntheticStreamer(
                    input_signal=SyntheticSignal().signal,
                    signal_collector=self.signal_collector, stream_freq=250)
        elif stream_origin == 'File':
            streamer = FileStreamer(
                    file_name=f'experiment_csv/pinch_close.csv',
                    signal_collector=self.signal_collector, stream_freq=250)
        else:
            raise Exception('No streamer was selected or incorrect name of streamer')
        return streamer










