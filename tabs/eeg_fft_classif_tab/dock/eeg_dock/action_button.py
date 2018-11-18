from PyQt5 import QtGui, QtCore
import numpy as np

class ActionButton:
    def __init__(self, layout, row, gv, ch, type='show avg'):
        self.gv = gv
        self.ch = ch

        self.timer = QtCore.QTimer()
        self.label = QtGui.QLabel()
        layout.addWidget(self.label, row, 2)

        actn = {'show avg': self.update_avg,
                'show max': self.update_max}
        self.actn_func = actn[type]

    @QtCore.pyqtSlot(bool)
    def show_action(self, checked):
        if checked:
            print('here')
            self.timer.timeout.connect(self.update_avg)
            self.timer.start(400)
        else:
            self.label.setText('')
            self.timer.stop()

    def update_avg(self):
        # Create the average label
        print('avg')
        avg_val =  f'{np.round(np.average(self.gv.data_queue[self.ch]), 2)} Vrms'
        self.label.setText(avg_val)


    def update_max(self):
        max_val = f'{np.round(np.max(self.gv.data_queue[self.ch]), 2)} Vrms'
        self.label.setText(max_val)