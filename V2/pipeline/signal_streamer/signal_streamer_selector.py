import os
from .from_synthetic_signal.synthetic_streamer import SyntheticStreamer
from .from_synthetic_signal.synthetic_signal import SyntheticSignal
from .from_file.file_streamer import FileStreamer


class SignalStreamerSelector:
    def __init__(self, stream_origin, signal_collector):
        self.stream_origin = stream_origin

        self.streamer = self._select_streamer(signal_collector)

    def _select_streamer(self, signal_collector):
        if self.stream_origin == 'Synthetic data':
            streamer = SyntheticStreamer(
                input_signal=SyntheticSignal(n_ch=8).signals,
                signal_collector=signal_collector)

        elif self.stream_origin == 'File':
            base_path = os.getcwd()
            file_path = 'pipeline/signal_streamer/from_file/experiment_csv/pinch_close.csv'
            path = os.path.join(base_path, file_path)

            streamer = FileStreamer(
                file_name=path, signal_collector=signal_collector)

        elif self.stream_origin == 'OpenBci':
            streamer = None

        else:
            raise Exception('No streamer was selected or incorrect name of streamer')

        return streamer







