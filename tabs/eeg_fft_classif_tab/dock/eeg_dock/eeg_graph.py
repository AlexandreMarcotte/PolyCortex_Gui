from data_processing_pipeline.filter import (butter_bandpass_filter,
                                             butter_lowpass_filter)
from collections import deque
import matplotlib.pyplot as plt


class EegGraph:
    def __init__(self, ch, q, gv, ts, curve, regions):
        self.ch = ch
        self.q = q
        self.gv = gv
        self.ts = ts
        self.curve = curve
        self.regions = regions

        self.i = 0

    def update_graph(self):
        self.update_eeg()
        self.i += 1
        if self.i % 100 == 0 and self.ch==0:
            # self.gv.data_queue[0] = deque(
            #     butter_bandpass_filter(self.gv.data_queue[0], lowcut=5,
            #                            highcut=30,fs=250), maxlen=self.gv.DEQUE_LEN)
            # y = butter_lowpass_filter(self.gv.data_queue[0], cutoff=6, fs=250, order=8)
            # plt.plot(y)
            # plt.show()
            pass

        # self.regions.detect_exp_event()

    def  update_eeg(self):
        # Time channel where we don't have to display any q
        if self.ch == 8:
            self.curve.setData(self.ts, self.q)

        else:
            self.curve.setData(self.q)
            # Detect the occurence of events by placing a region around them
            self.regions.detect_exp_event()