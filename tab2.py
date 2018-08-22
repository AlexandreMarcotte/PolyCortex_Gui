# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import *

from pyqtgraph.dockarea import *

import pyqtgraph as pg
from functools import partial

from random import randint


class Tab2(object):
    def __init__(self, main_window, tab2, timer_p300):
        # P300 experiment
        self.p300_char = ['A', 'B', 'C', 'D', 'E', 'F',
                          'G', 'H', 'I', 'J', 'K', 'L',
                          'M', 'N', 'O', 'P', 'Q', 'R',
                          'S', 'T', 'U', 'V', 'W', 'X',
                          'Y', 'Z', '1', '2', '3', '4',
                          '5', '6', '7', '8', '9', '0']
        self.show_p300 = True
        self.main_window = main_window
        # The second tab that was created inside the main window object
        self.tab2 = tab2
        self.timer_p300 = timer_p300

    def create_tab2(self):
        self.DARK_GREY = '#585858'  # (88, 88, 88)
        self.LIGHT_GREY = '#C8C8C8'  # (200, 200, 200)

        # Insert the tab layout inside the main window frame
        self.tab2.layout = QHBoxLayout(self.main_window)

        # Add a dock to the tab
        area = DockArea()
        self.tab2.layout.addWidget(area)
        self.P300_dock = Dock('Static graph dock')
        area.addDock(self.P300_dock)
        # Add the layout to the dock
        self.P300_layout = pg.LayoutWidget()
        self.P300_dock.addWidget(self.P300_layout)

        self.p300_plot = self.instantiate_p300_plot()
        row=1; col=0; rowspan=1; colspan=2
        self.P300_layout.addWidget(self.p300_plot, row, col, rowspan, colspan)

        # Start and stop button
        self.start_p300_button()
        self.stop_p300_button()
        # Result label
        self.show_p300_result()

        self.timer_p300.timeout.connect(self.update_p300)

        self.tab2.setLayout(self.tab2.layout)

    # ------------ P300 -------------
    def instantiate_p300_plot(self):
        p300_plot = pg.PlotWidget()
        p300_plot.setXRange(-2, 7)
        p300_plot.setYRange(-1, 5)
        p300_plot.hideAxis('bottom')
        p300_plot.hideAxis('left')
        return p300_plot

    def show_p300_result(self):
        result = QtGui.QLabel(f'Result: {"_ _ _ _ _"}')
        result.setFont(QtGui.QFont('SansSerif', pointSize=12))
        row=2; col=0; rowspan=1; colspan=1
        self.P300_layout.addWidget(result, row, col, rowspan, colspan)

    def update_p300(self):
        rand_row = randint(0, 5)
        rand_col = randint(0, 5)
        # clear the widget on the screen at every display to add a new batch
        self.p300_plot.clear()
        # Add all number to the plot
        for no, one_char in enumerate(self.p300_char):
            col = no % 6
            row = no // 6
            # Change the color on the row and column selected from the random
            # # Selected row
            if rand_col == col or rand_row == row:
                char_color = '#111'
            else:
                char_color = '#888'

            char = pg.TextItem(fill=(0, 0, 0), anchor=(0.5,0))
            html = f"""<span style="color: {char_color};
                       font-size: 56pt; ">
                       {one_char}"""
            char.setHtml(html)

            char.setPos(col, row)
            self.p300_plot.addItem(char)

    def start_p300_button(self):
        b_start = QtGui.QPushButton('START P300')
        b_start.setStyleSheet("background-color: rgba(255, 255, 255, 0.5)")
        b_start.clicked.connect(partial(self.start_p300))
        row=0; col=0; rowspan=1; colspan=1
        self.P300_layout.addWidget(b_start, row, col, rowspan, colspan)

    @pyqtSlot()
    def start_p300(self):
        self.timer_p300.start(200)

    def stop_p300_button(self):
        b_stop = QtGui.QPushButton('STOP P300')
        b_stop.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        b_stop.clicked.connect(partial(self.stop_p300))
        row = 0; col = 1; rowspan = 1; colspan = 1
        self.P300_layout.addWidget(b_stop, row, col, rowspan, colspan)

    @pyqtSlot()
    def stop_p300(self):
        self.timer_p300.stop()