# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import *

from pyqtgraph.dockarea import *

import pyqtgraph as pg
from functools import partial

from random import randint


class Tab4:
    def __init__(self, main_window, tab):
        self.main_window = main_window
        # The second tab that was created inside the main window object
        self.tab = tab

    def create_tab(self):
        # Insert the tab layout inside the main window frame
        self.tab.layout = QHBoxLayout(self.main_window)
        # Add docs to the tab
        self.area = DockArea()
        self.tab.layout.addWidget(self.area)

        right_hand_dock = HandDock(self.area, 'Electrode #1')
        for elect_no in range(3):
            HandDock(self.area, f'Electrode #{elect_no+2}',
                     other_hand_dock=right_hand_dock.dock)

        self.tab.setLayout(self.tab.layout)


class HandDock:
    def __init__(self, area, hand_side, other_hand_dock=None):
        self.area = area
        self.hand_side = hand_side
        self.other_hand_dock = other_hand_dock
        self.elect_num = 0
        # Create dock
        self.init_hand_dock()
        self.create_total_hand_dock()

    def init_hand_dock(self):
        self.dock = Dock(self.hand_side)
        if self.other_hand_dock:
            self.area.addDock(self.dock, 'above', self.other_hand_dock)
        else:
            self.area.addDock(self.dock)
        # Add the layout to the dock
        self.hand_layout = pg.LayoutWidget()
        self.dock.addWidget(self.hand_layout)

    def create_total_hand_dock(self):
        # Create electrod 1 layout:
        self.create_one_electrod_layout(self.hand_layout)
        # Create electrod 2 layout:
        # self.elect_num += 1
        # self.elect_2_layout = QGridLayout()
        # self.elect_2_widget = QWidget()
        # self.elect_2_widget.setLayout(self.elect_2_layout)
        # self.create_one_electrod_layout(self.elect_2_layout)
        # Add the electrodes layout split by the Qsplitter
        # self.add_splitter_between_electrodes()
        # self.hand_layout.addWidget(self.elect_layout)

    def create_one_electrod_layout(self, layout):
        self.add_title(layout)
        self.add_avg_class_apparance_graph(layout)
        self.add_one_class_visualisation_graph(layout)
        self.add_classification_certitude_graph(layout)
        self.add_slider(layout)

    def add_title(self, layout):
        title = QtGui.QLabel(f'Electrode #{self.elect_num+1}')
        title.setStyleSheet("""font: 12pt; background-color: rgb(50,50,50);
                               margin:5px; border:1px solid rgb(100, 100, 150); """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        row=0; col=1; rowspan=1; colspan=2
        layout.addWidget(title, row, col, rowspan, colspan)

    def add_one_class_visualisation_graph(self, layout):
        avg_class_plot = pg.PlotWidget()
        avg_class_plot.plotItem.setTitle(f'All data')
        row=1; col=0; rowspan=1; colspan=1
        layout.addWidget(avg_class_plot, row, col, rowspan, colspan)

    def add_classification_certitude_graph(self, layout):
        class_certitude_graph = pg.PlotWidget()
        row=2; col=0; rowspan=1; colspan=1
        class_certitude_graph.plotItem.setTitle(f'Certitude classification')
        layout.addWidget(class_certitude_graph, row, col, rowspan,
                                   colspan)

    def add_slider(self, layout):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        row=0; col=0; rowspan=1; colspan=1
        layout.addWidget(slider, row, col, rowspan, colspan)

    def add_avg_class_apparance_graph(self, layout):
        one_class_plot = pg.PlotWidget()
        one_class_plot.plotItem.setTitle(f'avg class appearance graph')
        row=1; col=1; rowspan=2; colspan=2
        layout.addWidget(one_class_plot, row, col, rowspan, colspan)

    # def add_splitter_between_electrodes(self):
    #     # Create a splitter for the electrodes
    #     electrodes_spliter = QSplitter(Qt.Vertical)
    #     electrodes_spliter.addWidget(self.elect_1_widget)
    #     electrodes_spliter.addWidget(self.elect_2_widget)
    #     self.hand_layout.addWidget(electrodes_spliter)



