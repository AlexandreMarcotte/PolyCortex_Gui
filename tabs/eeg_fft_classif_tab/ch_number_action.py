from PyQt5 import QtGui, QtCore


class ChNumberAction:
    def __init__(self, timers_eeg, ch):
        self.timers_eeg = timers_eeg
        self.ch = ch

    @QtCore.pyqtSlot(bool)
    def stop_ch(self, checked):
        if checked:
            self.timers_eeg[self.ch].stop()
        else:
            self.timers_eeg[self.ch].start()