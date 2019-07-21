from threading import Thread, Lock, Event
from PyQt5.QtCore import pyqtSlot
# --My Packages--
from ..pipeline.signal_streamer.signal_collector import SignalCollector
# from ..pipeline.signal_streamer.from_open_bci.from_open_bci import SampleDataFromOpenBci
from .pipeline_stages.fft_stage.fft_stage import FftStage
from ..pipeline.pipeline_stages.filter_stage.filter_stage import FilterStage
from V2.pipeline.pipeline_stages.filter_stage.filter import Filter
from .signal_streamer.signal_streamer_selector import SignalStreamerSelector


class Pipeline: #(Thread):
    def __init__(self):
        super().__init__()
        event = Event()

        self.signal_collector = SignalCollector(len=1500, event=event)

        # self.signal_collector.filled_new_data_into_queue.connect(
        #     self.signal_collector.print_shit)

        # self.streamer = self.start_signal_streamer(stream_origin='File')
        self.streamer = SignalStreamerSelector(
            stream_origin='File', # 'Synthetic data',
            signal_collector=self.signal_collector).streamer
        # self.streamer.start()
        # Filter
        self.filter_stage = FilterStage(
            signal_collector=self.signal_collector,
            filters={
                    # 'bandpass':
                    #      Filter(cut_freq=(3, 122), filter_type='bandpass'),
                     'bandstop':
                         Filter(cut_freq=(55, 65), filter_type='bandstop')
                    },
            event=event
        )
        """
        """
        # FFT
        self.fft_stage = FftStage(
            # input=self.signal_collector.input,
            input=self.filter_stage.output,
            timestamps=self.signal_collector.timestamps, remove_first_freq=1)

    # def run(self):

    def start(self):
        self.streamer.start()
        self.filter_stage.start()
        self.fft_stage.start()


