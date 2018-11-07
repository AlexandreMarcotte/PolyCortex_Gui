# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import *

from pyqtgraph.dockarea import *

import pyqtgraph as pg
from functools import partial

from random import randint

# -- My packages --
from .action import Action
from .p300 import P300Dock
from app.colors import *


class ExperimentTab:
    def __init__(self, main_window, tab_w, gv):
        self.main_window = main_window
        # The second tab that was created inside the main window object
        self.tab_w = tab_w
        self.gv = gv
        # Create the tab itself
        self.create_tab()

    def create_tab(self):
        self.DARK_GREY = '#585858'  # hexa
        self.LIGHT_GREY = '#C8C8C8'
        # Insert the tab layout inside the main window frame
        self.tab_w.layout = QHBoxLayout(self.main_window)
        # Add docs to the tab
        self.area = DockArea()
        self.tab_w.layout.addWidget(self.area)
        # EMG
        emg_dock = EmgDock(self.area, self.gv)
        # N100
        n100_dock = N100Dock(self.area, emg_dock.emg_dock)
        n100_dock.create_n100_dock()
        # P300
        p300_dock = P300Dock(self.area, emg_dock.emg_dock)
        p300_dock.create_p300_dock()

        self.tab_w.setLayout(self.tab_w.layout)


class N100Dock:
    def __init__(self, area, emg_dock):
        self.area = area
        self.emg_dock = emg_dock

    def create_n100_dock(self):
        self.n100_dock = Dock('N100 experiment')
        self.area.addDock(self.n100_dock, 'above', self.emg_dock)

class EmgDock:
    def __init__(self, area, gv):
        # Plot variables
        self.area = area
        self.gv = gv
        # Variables
        self.actions = []
        self.action_name = 'ACTION'
        self.num_of_action = 20
        self.action_itt = 0

        self.end_experiment = False

        self.create_emg_dock()

        self.init_spawn_timer()
        self.init_plot_timer()

    def create_emg_dock(self):
        self.emg_dock = Dock('EMG experiment')
        self.area.addDock(self.emg_dock)
        # Add the layout to the dock
        self.emg_layout = pg.LayoutWidget()
        self.emg_dock.addWidget(self.emg_layout)

        self.instantiate_emg_plot()
        row=1; col=0; rowspan=1; colspan=2
        self.emg_layout.addWidget(self.emg_plot, row, col, rowspan, colspan)
        # Start and stop button
        self.start_emg_button()
        self.stop_emg_button()

    def instantiate_emg_plot(self):
        self.emg_plot = pg.PlotWidget()
        self.emg_plot.setYRange(0.7, 6.5)
        self.emg_plot.setXRange(0, 20)
        self.emg_plot.plotItem.hideAxis('bottom')
        self.emg_plot.plotItem.hideAxis('left')
        # Vertical and horizontal delineation lines
        # vLine = pg.InfiniteLine(angle=90, pos=10, movable=False)
        hLine = pg.InfiniteLine(angle=0, pos=1.5, movable=False)
        # self.emg_plot.addItem(vLine, ignoreBounds=True)
        self.emg_plot.addItem(hLine, ignoreBounds=True)

    def init_spawn_timer(self):
        self.spawn_timer = QtCore.QTimer()
        self.spawn_timer.timeout.connect(self.update_spawn)

    def init_plot_timer(self):
        self.plot_timer = QtCore.QTimer()
        self.plot_timer.timeout.connect(self.update_plot)

    def update_spawn(self):
        # Stop spawning value when we reach the number of experiment events
        if self.action_itt < self.num_of_action:
            # Create a new action:
            action = Action(actn_txt=self.action_name, wait_txt='WAIT...',
                            y_pos=6.5, x_pos=10)
            # Plot this new action
            self.emg_plot.addItem(action.plot)
            # Add it to the list of actions
            self.actions.append(action)
            self.action_itt += 1
        else:
            self.end_experiment = True

    def update_plot(self):
        for action in self.actions:
            # update the listed position of the action
            action.y_pos -= 0.04
            # If the action text event is bellow the horiz. activation line
            if 0 <= action.y_pos <= 1.5 and action.wait:
                self.gv.experiment_type[0] = 1
                action.activate_html()
                action.wait = False
            # update the position of the action
            action.plot.setPos(action.x_pos, action.y_pos)
            # If the action leave the screen remove it
            if action.y_pos < 0:
                self.emg_plot.removeItem(self.actions[0].plot)
                self.actions.pop(0)
        # Stop spawning value when we reach the number of experiment events
        if self.actions == [] and self.end_experiment:
            print('End of EMG Experiment reached')
            self.show_end_txt()
            self.stop_emg()

    def show_end_txt(self):
        self.end_txt = pg.TextItem(anchor=(0, 0), fill=(0, 0, 0, 0))
        self.end_txt_html = f"""<div style="text-align: center">
                               <br><span style="color: {'#EEE'};
                               font-size: 30pt;">{'End of experiment...'}
                               </span></div>"""
        self.end_txt.setHtml(self.end_txt_html)
        self.end_txt.setPos(7, 5)
        self.emg_plot.addItem(self.end_txt)

    def start_emg_button(self):
        b_start = QtGui.QPushButton('START EMG')
        b_start.setStyleSheet(f"background-color: {white}")
        b_start.clicked.connect(partial(self.start_emg))
        self.emg_layout.addWidget(b_start, 0, 0)

    @pyqtSlot()
    def start_emg(self):
        self.spawn_timer.start(1200)
        self.plot_timer.start(30)

    def stop_emg_button(self):
        b_stop = QtGui.QPushButton('STOP EMG')
        b_stop.setStyleSheet(f"background-color: {black}")
        b_stop.clicked.connect(partial(self.stop_emg))
        self.emg_layout.addWidget(b_stop, 0, 1)

    @pyqtSlot()
    def stop_emg(self):
        self.spawn_timer.stop()
        self.plot_timer.stop()