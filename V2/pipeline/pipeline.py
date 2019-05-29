from V2.pipeline.generate_signal.signal_collector import SignalCollector
from V2.pipeline.generate_signal.signal_streamer import SignalStreamer
from .generate_signal.file_streamer import FileStreamer
from V2.pipeline.pipeline_stages.filter_stage.filter_stage import FilterStage
from V2.pipeline.generate_signal.from_synthetic_signal.from_synthetic_signal import SyntheticSignal
from .pipeline_stages.fft_stage.fft_stage import FftStage


class Pipeline:
    def __init__(self):
        self.start()

    def start(self):
        self.signal_collector = SignalCollector(len=1000)
        self.streamer = self.start_signal_streamer('File')
        # Filter
        self.filter_stage = FilterStage(input=self.signal_collector.input)
        self.filter_stage.start()
        # FFT
        self.fft_stage = FftStage(
                input=self.filter_stage.input,
                timestamps=self.signal_collector.timestamps)
        self.fft_stage.start()

    def start_signal_streamer(self, stream_origin='Synthetic data'):
        if stream_origin == 'Synthetic data':
            streamer = SignalStreamer(
                    input_signal=SyntheticSignal().signal,
                    signal_collector=self.signal_collector, stream_freq=250)
        elif stream_origin == 'File':
            streamer = FileStreamer(
                    file_name=f'experiment_csv/pinch_close.csv',
                    signal_collector=self.signal_collector, stream_freq=250)
        return streamer
