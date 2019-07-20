from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import numpy as np
from collections import deque
# --My packages--
from .btn import Btn
from V2.utils.colors import Color


class LabelBtn(Btn):
    def __init__(self, name, tip=None, conn_func='avg', plot=None):
        super().__init__(
                name, color=Color.dark_blue_tab, toggle=True, tip=tip, max_width=29,
                min_width=15, max_height=39, txt_color=Color.white, font_size=11)

        self.plot = plot
        # self.conn_func = conn_func
        actn = {'avg': self.update_avg,
                'max': self.update_max}
                # 'filter': self.change_filter_window_size}
        self.actn_func = actn[conn_func]
        # if conn_func == 'filter':
        #     self.filter_region = pg.LinearRegionItem([0, 0])
        #     self.filter_region.setBrush(blue)
        #     plot_creator.plots[ch].addItem(self.filter_region)

        self._init_timer()
        self.label = self._create_label()
        self._connect()

    def _connect(self):
        self.clicked.connect(self.show_action)

    def _create_label(self):
        style = ("""QLabel {background-color: rgba(0, 0, 0, 0); 
                    color: rgba(180, 180, 180, 1)}""")
        label = QLabel('')
        label.setStyleSheet(style)
        return label

    def _init_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.actn_func)

    @QtCore.pyqtSlot(bool)
    def show_action(self, checked):
        if checked:
            self.timer.start(200)
            # if self.conn_func == 'filter':
            #     self.filter_region.setRegion([0, self.gv.DEQUE_LEN])
        else:
            self.label.setText('')
            self.timer.stop()
    # def change_filter_window_size(self):
    #     min_r, max_r = self.filter_region.getRegion()
    #     self.gv.filter_max_bound = int(self.gv.DEQUE_LEN - min_r)
    #     print('max_bound', self.gv.filter_max_bound)
    #     self.gv.filter_min_bound = int(self.gv.DEQUE_LEN - max_r)
    #     print('min bound', self.gv.filter_min_bound)

        # print('min_r', self.gv.filter_max_bound,
        #       'max_r', self.gv.filter_min_bound)
    def update_avg(self):
        """"Create the average label"""
        avg_val = f'{np.round(np.average(self.plot.signals), 2)} Vrms'
        self.label.setText(avg_val)

    def update_max(self):
        """Create the max label"""
        max_val = f'{np.round(np.max(self.plot.signals), 2)} Vrms'
        self.label.setText(max_val)
