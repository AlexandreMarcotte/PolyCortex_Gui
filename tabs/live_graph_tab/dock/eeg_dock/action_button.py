from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import numpy as np


class ActionButton:
    def __init__(self, layout, row, gv, ch, conn_func='avg'):
        self.gv = gv
        self.ch = ch

        self.timer = QtCore.QTimer()
        self.label = self.create_label()
        layout.addWidget(self.label, row, 6)

        actn = {'avg': self.update_avg,
                'max': self.update_max}
        self.actn_func = actn[conn_func]

    def create_label(self):
        style = ("""QLabel {background-color: rgba(0, 0, 0, 0); 
                         color: rgba(180, 180, 180, 1)}""")
        label = QLabel()
        label.setStyleSheet(style)
        return label

    @QtCore.pyqtSlot(bool)
    def show_action(self, checked):
        if checked:
            self.timer.timeout.connect(self.actn_func)
            self.timer.start(300)
        else:
            self.label.setText('')
            self.timer.stop()

    def update_avg(self):
        """"Create the average label"""
        avg_val =  f'{np.round(np.average(self.gv.data_queue[self.ch]), 2)} Vrms'
        self.label.setText(avg_val)
        print(self.ch, 'avg')

    def update_max(self):
        """Create the max label"""
        max_val = f'{np.round(np.max(self.gv.data_queue[self.ch]), 2)} Vrms'
        print(self.ch, 'max')
        self.label.setText(max_val)