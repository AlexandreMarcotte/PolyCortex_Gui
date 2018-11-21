# -- GEneral Packages --
from PyQt5.QtCore import Qt, pyqtSlot
from pyqtgraph.dockarea import *
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from functools import partial
# -- My Packages --
from .action import Action
from .experiment import Experiment


class EmgDock(Experiment):
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

        self.instantiate_emg_plot()
        self.emg_dock.addWidget(self.emg_plot, 1, 0, 1, 2)
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
        hLine = pg.InfiniteLine(angle=0, pos=1.5, movable=False)
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
                # self.gv.experiment_type[0] = action.type_num
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
        b_start.setStyleSheet("background-color: rgba(200, 200, 200, 0.5)")
        b_start.clicked.connect(partial(self.start_emg))
        self.emg_dock.addWidget(b_start, 0, 0)

    @pyqtSlot()
    def start_emg(self):
        self.spawn_timer.start(1200)
        self.plot_timer.start(30)

    def stop_emg_button(self):
        b_stop = QtGui.QPushButton('STOP EMG')
        b_stop.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        b_stop.clicked.connect(partial(self.stop_emg))
        self.emg_dock.addWidget(b_stop, 0, 1)

    @pyqtSlot()
    def stop_emg(self):
        self.spawn_timer.stop()
        self.plot_timer.stop()