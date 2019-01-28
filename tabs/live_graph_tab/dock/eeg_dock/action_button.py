from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import numpy as np
import pyqtgraph as pg
from app.colors import *


class ActionButton:
    def __init__(self, layout, row, gv, ch, conn_func='avg',
                 plot_creator=None):
        self.gv = gv
        self.ch = ch
        self.conn_func = conn_func

        self.label = self.create_label()
        layout.addWidget(self.label, row, 6)

        actn = {'avg': self.update_avg,
                'max': self.update_max,
                'filter': self.change_filter_window_size}

        self.actn_func = actn[conn_func]

        if conn_func == 'filter':
            self.filter_region = pg.LinearRegionItem([0, 0])
            self.filter_region.setBrush(blue)
            plot_creator.plots[ch].addItem(self.filter_region)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.actn_func)

    def create_label(self):
        style = ("""QLabel {background-color: rgba(0, 0, 0, 0); 
                    color: rgba(180, 180, 180, 1)}""")
        label = QLabel()
        label.setStyleSheet(style)
        return label

    @QtCore.pyqtSlot(bool)
    def show_action(self, checked):
        if checked:
            self.timer.start(300)
            if self.conn_func == 'filter':
                self.filter_region.setRegion([0, self.gv.DEQUE_LEN])
        else:
            self.label.setText('')
            self.timer.stop()

    def change_filter_window_size(self):
        min_r, max_r = self.filter_region.getRegion()
        self.gv.filter_max_bound = int(self.gv.DEQUE_LEN - min_r)
        print('max_bound', self.gv.filter_max_bound)
        self.gv.filter_min_bound = int(self.gv.DEQUE_LEN - max_r)
        print('min bound', self.gv.filter_min_bound)
        # print('min_r', self.gv.filter_max_bound,
        #       'max_r', self.gv.filter_min_bound)

    def update_avg(self):
        """"Create the average label"""
        avg_val = f'{np.round(np.average(self.gv.data_queue[self.ch]), 2)} Vrms'
        self.label.setText(avg_val)

    def update_max(self):
        """Create the max label"""
        max_val = f'{np.round(np.max(self.gv.data_queue[self.ch]), 2)} Vrms'
        self.label.setText(max_val)