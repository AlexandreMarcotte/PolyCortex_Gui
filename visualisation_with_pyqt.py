# -*- coding: utf-8 -*-

# PLOTING the EEG data
# Graph the data
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap

# from pyqtgraph.Qt import QtGui
import os
import numpy as np
from collections import deque

# My packages
from frequency_counter import FrequencyCounter
# -- Tabs --
from tab1 import Tab1
from tab2 import Tab2
from tab3 import Tab3
from tab4 import Tab4

class OpenBciGui(QMainWindow):

    def __init__(self, data_queue, t_queue, t_init, n_data_created):
        super(OpenBciGui, self).__init__()
        self.setWindowTitle('--OpenBCI graph--')
        self.setWindowIcon(QtGui.QIcon('polycortex_logo.png'))
        # Add a menu bar
        self.create_menu_bar()
        # message at the bottom
        self.statusBar().showMessage('Running the experiment ...')

        self.simple_graph = Tabs(data_queue, t_queue,
                                 t_init, n_data_created)                        # TODO: ALEXM divide this part in many objects
        self.setCentralWidget(self.simple_graph)

        self.show()

    def create_menu_bar(self):
        main_menu = self.menuBar()
        # File
        self.menuFile = QMenu(title='Stream from...')
        # # Action
        self.openbci = QtGui.QAction('OpenBci')                                # TODO: ALEXM Utiliser une liste déroulante plutot
        self.openbci.setShortcut('Ctrl+O')
        self.openbci.setStatusTip('Stream data from Openbci...')
        self.fake_data = QtGui.QAction('Fake data')
        self.fake_data.setStatusTip('Stream data from artificially generated data...')
        self.from_file = QtGui.QAction('From file')
        self.from_file.setStatusTip('Stream data from previously saved file...')

        # self.quit_action.triggered.connect(....)
        self.menuFile.addAction(self.openbci)
        self.menuFile.addAction(self.fake_data)
        self.menuFile.addAction(self.from_file)

        main_menu.addMenu(self.menuFile)


class Tabs(QWidget):
    def __init__(self, data_queue, t_queue, t_init, n_data_created):
        """
        """
        super(Tabs, self).__init__()
        self.data_queue = data_queue
        self.N_CH = len(self.data_queue)
        self.t_queue = t_queue
        self.t_init = t_init
        self.n_data_created = n_data_created

        self.timer_p300 = QtCore.QTimer()

        self.init_font()

        self.init_win()

    def init_font(self):
        self.font = QtGui.QFont()
        self.font.setPointSize(50)

    def init_win(self):
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "EEG & FFT live graph")
        self.tabs.addTab(self.tab2, "P300 experiment")
        self.tabs.addTab(self.tab3, "EEG static graph")
        self.tabs.addTab(self.tab4, "3D representation")
        # self.tabs.addTab(self.tab5, "Mini Game")

        # Compose tabs
        # - Tab 1
        tab_1 = Tab1(self, self.tab1, self.n_data_created, self.data_queue,
                     self.t_queue, self.t_init)
        tab_1.create_tab1()
        # - Tab 2
        tab_2 = Tab2(self, self.tab2, self.timer_p300)
        tab_2.create_tab2()
        # - Tab 3
        tab_3 = Tab3(self, self.tab3, self.data_queue)
        tab_3.create_tab3()
        # - Tab 4
        tab_4 = Tab4(self, self.tab4)
        tab_4.create_tab4()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)