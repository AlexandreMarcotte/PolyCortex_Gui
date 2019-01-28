# -- GEneral Packages --
from PyQt5.QtCore import Qt, pyqtSlot
from pyqtgraph.dockarea import *
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from functools import partial
# -- My Packages --
from .action import Action
from tabs.experiment_tab.experiment import Experiment


class EmgDock(Experiment):
    def __init__(self, area, gv):
        super().__init__()
        self.area = area
        self.gv = gv

        self.actions = []
        self.action_name = 'ACTION'
        self.num_of_action = 100
        self.action_itt = 0

        self.end_experiment = False

        self.create_emg_dock()

        self.init_spawn_timer()
        self.init_plot_timer()

    def create_emg_dock(self):
        self.emg_dock = Dock('EMG experiment')
        self.area.addDock(self.emg_dock)

        self.layout = pg.LayoutWidget()
        self.emg_dock.addWidget(self.layout)

        self.plot = self.create_plot()
        self.layout.addWidget(self.plot, 1, 0, 1, 2)
        # Start and stop button
        self.create_start_b('EMG')
        self.create_stop_b('EMG')

    def create_plot(self, xs=(0, 20), ys=(0.7, 6.5)):
        plot = super().create_plot(xs, ys)
        # Horizontal delineation lines to activate an event
        hLine = pg.InfiniteLine(angle=0, pos=1.5, movable=False)
        plot.addItem(hLine, ignoreBounds=True)
        return plot

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
            action = Action(
                    actn_txt=self.action_name, wait_txt='WAIT...', y_pos=6.5,
                    x_pos=10)
            # Plot this new action
            self.plot.addItem(action.plot)
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
                self.gv.experiment_type = 1  # 1 meaning that an event happen
                                             # (binary scenario)
                action.activate_html()
                action.wait = False
            # update the position of the action
            action.plot.setPos(action.x_pos, action.y_pos)
            # If the action leave the screen remove it
            if action.y_pos < 0:
                self.plot.removeItem(self.actions[0].plot)
                self.actions.pop(0)
        # Stop spawning value when we reach the number of experiment events
        if self.actions == [] and self.end_experiment:
            print('End of EMG Experiment reached')
            self.show_end_txt()
            self.stop()

    def show_end_txt(self):
        self.end_txt = pg.TextItem(anchor=(0, 0), fill=(0, 0, 0, 0))
        self.end_txt_html = f"""<div style="text-align: center">
                                <br><span style="color: {'#EEE'};
                                font-size: 30pt;">{'End of experiment...'}
                                </span></div>"""
        self.end_txt.setHtml(self.end_txt_html)
        self.end_txt.setPos(7, 5)
        self.plot.addItem(self.end_txt)

    @pyqtSlot()
    def start(self):
        self.plot_timer.start(30)
        self.spawn_timer.start(1200)

    @pyqtSlot()
    def stop(self):
        self.plot_timer.stop()
        self.spawn_timer.stop()
