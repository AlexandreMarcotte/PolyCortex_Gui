from PyQt5 import QtGui, QtCore
import numpy as np

class ActionButton:
    def __init__(self, gv, layout, b_n, ch, pos):
        self.gv = gv
        self.b_n = b_n
        self.ch = ch
        # self.tab = tab
        self.layout = layout
        self.pos = pos
        self.style = ("""QLabel {background-color: rgba(0, 0, 0, 0); 
                         color: rgba(180, 180, 180, 1)}""")
        # Create timer
        self.timer_avg = QtCore.QTimer()
        self.timer_max = QtCore.QTimer()
        # Create labels
        self.avg_label = QtGui.QLabel()
        self.max_label = QtGui.QLabel()

        self.create_avg_button()
        self.create_max_button()

    def create_avg_button(self):
        self.avg_label.setStyleSheet(self.style)
        # Set position of the label
        row=self.pos; col=2; rowspan=1; colspan=1
        self.layout.addWidget(self.avg_label, row, col, rowspan, colspan)

    def update_avg(self):
        # Create the average label
        avg_val = ' '*70 + f'{np.round(np.average(self.gv.data_queue[self.ch]), 2)} Vrms'
        self.avg_label.setText(avg_val)

    def create_max_button(self):
        # Create the average label                                             # TODO: ALEXM Enlever la répétition
        self.max_label.setStyleSheet(self.style)
        # Set position of the label
        self.layout.addWidget(self.max_label, self.pos, 2)

    def update_max(self):
        max_val = ' ' *70 + f'{np.round(np.max(self.gv.data_queue[self.ch]), 2)} Vrms'
        self.max_label.setText(max_val)

    @QtCore.pyqtSlot(bool)                                                            # TODO: ALEXM remove this duplicate
    def show_avg(self, checked):
        if checked:
            # Update the average label
            self.timer_avg.timeout.connect(self.update_avg)
            self.timer_avg.start(400)
        else:
            self.avg_label.setText('')
            self.timer_avg.stop()

    @QtCore.pyqtSlot(bool)
    def show_max(self, checked):
        if checked:
            # Update the average label
            self.timer_max.timeout.connect(self.update_max)
            self.timer_max.start(400)
        else:
            self.max_label.setText('')
            self.timer_max.stop()