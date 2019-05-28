from V2.pipeline.generate_signal.signal_collector import SignalCollector
from V2.pipeline.generate_signal.signal_streamer import SignalStreamer
from V2.pipeline.pipeline_stages.filter_stage.filter_stage import FilterStage
from V2.pipeline.generate_signal.from_synthetic_signal.from_synthetic_signal import SyntheticSignal
from .pipeline_stages.fft_stage.fft_stage import FftStage


class Pipeline:
    def __init__(self):
        self.start()

    def start(self):
        self.signal_collector = SignalCollector(len=1000)

        self.signal_streamer = SignalStreamer(
                input_signal=SyntheticSignal().signal,
                signal_collector=self.signal_collector, stream_freq=250)
        # Filter
        self.filter_stage = FilterStage(input=self.signal_collector.input)
        self.filter_stage.start()
        # FFT
        self.fft_stage = FftStage(
                input=self.filter_stage.input,
                timestamps=self.signal_collector.timestamps)
        self.fft_stage.start()
