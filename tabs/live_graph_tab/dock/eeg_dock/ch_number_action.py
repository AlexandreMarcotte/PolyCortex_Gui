from PyQt5 import QtGui, QtCore


class ChNumberAction:
    def __init__(self, timers, ch):
        self.timers = timers
        self.ch = ch

    @QtCore.pyqtSlot(bool)
    def stop_ch(self, checked):
        if checked:
            self.timers[self.ch].stop()
        else:
            self.timers[self.ch].start()