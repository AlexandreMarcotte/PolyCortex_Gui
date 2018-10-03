# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import *

from pyqtgraph.dockarea import *

import pyqtgraph as pg
from functools import partial

from random import randint

# My packages
from init_variables import InitVariables


class Tab2:
    def __init__(self, main_window, tab2, experiment_type, experiment_queue):
        self.main_window = main_window
        # The second tab that was created inside the main window object
        self.tab2 = tab2
        self.experiment_type = experiment_type
        self.experiment_queue = experiment_queue

    def create_tab2(self):
        self.DARK_GREY = '#585858'  # (88, 88, 88)
        self.LIGHT_GREY = '#C8C8C8'  # (200, 200, 200)
        # Insert the tab layout inside the main window frame
        self.tab2.layout = QHBoxLayout(self.main_window)
        # Add docs to the tab
        self.area = DockArea()
        self.tab2.layout.addWidget(self.area)
        # EMG
        emg_dock = EmgDock(self.area, self.experiment_type)
        # N100
        n100_dock = N100Dock(self.area, emg_dock.emg_dock)
        n100_dock.create_n100_dock()
        # P300
        p300_dock = P300Dock(self.area, emg_dock.emg_dock)
        p300_dock.create_p300_dock()

        self.tab2.setLayout(self.tab2.layout)


class Action:
    def __init__(self, action_txt, wait_txt, pos, type, color='#FF0'):
        self.pos = pos
        self.type_dict = {'Left PINCH': 1, 'Left CLOSE': 2,
                          'Right PINCH': 3, 'Right CLOSE': 4}
        self.type_num = self.type_dict[type]
        self.column = 5 * (self.type_num-1) + 2.5
        self.pos = pos
        self.action_txt = action_txt
        self.wait_txt = wait_txt
        self.color = color
        self.plot_obj = None
        self.is_waiting = True

        self.init_action()

    def init_action(self):
        self.plot_obj = pg.TextItem(anchor=(0.5, 1), angle=0,
                                    border='w', fill=(0, 0, 255, 100))
        self.action_html = f"""<div style="text-align: center">
                               <span style="color: #FFF;">{self.action_txt}
                               </span><br><span style="color: {self.color};
                               font-size: 14pt;">{self.wait_txt}</span></div>"""
        self.plot_obj.setHtml(self.action_html)
        self.plot_obj.setPos(self.column, self.pos)

    def activate_html(self):
        """Change the color  and text of the action text to indicate it's
           activation"""
        self.color = '#0FF'
        self.wait_txt = 'NOW!'
        self.html = f"""<div style="text-align: center">
                        <span style="color: #FFF;">{self.action_txt}
                        </span><br><span style="color: {self.color};
                        font-size: 16pt;">{self.wait_txt}</span></div>"""
        self.plot_obj.setHtml(self.html)


class N100Dock:
    def __init__(self, area, emg_dock):
        self.area = area
        self.emg_dock = emg_dock

    def create_n100_dock(self):
        self.n100_dock = Dock('N100 experiment')
        self.area.addDock(self.n100_dock, 'above', self.emg_dock)

class EmgDock:
    def __init__(self, area, experiment_type):
        # Plot variables
        self.area = area
        self.experiment_type = experiment_type
        # Variables
        self.N_ACTION = 4
        self.actions = []
        self.all_types = ['Left PINCH', 'Left CLOSE', 'Right PINCH', 'Right CLOSE']
        # How to read the action_order that is planned:
        # [first batch, _ ], [second batch, _ ], [third batch, _ ] ...
        # [ _, fifth batch], [ _, sixth batch] ...
        # The number tells the number of this type to spawn in the curent batch
        # Every item needs to have the same number of number in its list
        self.action_order = {'Left PINCH': [25, 25], 'Left CLOSE': [25, 25],
                             'Right PINCH': [25, 25], 'Right CLOSE': [25, 25]}
        self.next_action = []
        self.action_itt = 0
        self.init_action_order()

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
        # self.stop_emg_button()

    def instantiate_emg_plot(self):
        self.emg_plot = pg.PlotWidget()
        self.emg_plot.setYRange(0, 6.5)
        self.emg_plot.setXRange(0, 20)
        self.emg_plot.plotItem.hideAxis('bottom')
        self.emg_plot.plotItem.hideAxis('left')
        # Vertical and horizontal delineation lines
        vLine = pg.InfiniteLine(angle=90, pos=10, movable=False)
        hLine = pg.InfiniteLine(angle=0, pos=1.5, movable=False)
        self.emg_plot.addItem(vLine, ignoreBounds=True)
        self.emg_plot.addItem(hLine, ignoreBounds=True)

    def init_action_order(self):
        for n in range(len(self.action_order['Left PINCH'])):
            for action_name, num in self.action_order.items():
                for _ in range(num[n]):
                    self.next_action.append(action_name)

    def init_spawn_timer(self):
        self.spawn_timer = QtCore.QTimer()
        self.spawn_timer.timeout.connect(self.update_spawn)

    def init_plot_timer(self):
        self.plot_timer = QtCore.QTimer()
        self.plot_timer.timeout.connect(self.update_plot)

    def update_spawn(self):
        try:
            self.type = self.next_action[self.action_itt]
        except IndexError:
            print('End of EMG Experiment')
            # self.stop_emg()
        # Create a new action:
        action = Action(action_txt=self.type, wait_txt='WAIT...', pos=6.5,
                        type=self.type)
        # Plot this new action
        self.emg_plot.addItem(action.plot_obj)
        # Add it to the list of actions
        self.actions.append(action)
        # Incremente the action_itt so that we have the next action planified next
        self.action_itt += 1

    def update_plot(self):
        for action in self.actions:
            # update the listed position of the action
            action.pos -= 0.05
            # If the action text went is bellow the activation line
            if 0 <= action.pos <= 1.5 and action.is_waiting:
                print('exp type', self.experiment_type)
                self.experiment_type[0] = action.type_num
                action.activate_html()
                action.is_waiting = False
            # update the position of the action
            action.plot_obj.setPos(action.column, action.pos)
            # If the action is about to get out of the screen remove it
            if len(self.actions) > 10:
                self.emg_plot.removeItem(self.actions[0].plot_obj)
                self.actions.pop(0)

    def start_emg_button(self):
        b_start = QtGui.QPushButton('START EMG')
        b_start.setStyleSheet("background-color: rgba(255, 255, 255, 0.5)")
        b_start.clicked.connect(partial(self.start_emg))
        row=0; col=0; rowspan=1; colspan=1
        self.emg_layout.addWidget(b_start, row, col, rowspan, colspan)

    @pyqtSlot()
    def start_emg(self):
        self.spawn_timer.start(1200)
        self.plot_timer.start(30)

    def stop_emg_button(self):
        b_stop = QtGui.QPushButton('STOP EMG')
        b_stop.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        b_stop.clicked.connect(partial(self.stop_emg))
        row = 0; col = 1; rowspan = 1; colspan = 1
        self.emg_layout.addWidget(b_stop, row, col, rowspan, colspan)

    @pyqtSlot()
    def stop_emg(self):
        self.spawn_timer.stop()
        self.plot_timer.stop()


class P300Dock:
    def __init__(self, area, emg_dock):
        self.p300_char = ['A', 'B', 'C', 'D', 'E', 'F',
                          'G', 'H', 'I', 'J', 'K', 'L',
                          'M', 'N', 'O', 'P', 'Q', 'R',
                          'S', 'T', 'U', 'V', 'W', 'X',
                          'Y', 'Z', '1', '2', '3', '4',
                          '5', '6', '7', '8', '9', '0']
        self.show_p300 = True
        self.area = area
        self.timer_p300 = QtCore.QTimer()

        self.emg_dock = emg_dock

    def create_p300_dock(self):
        self.P300_dock = Dock('P300 experiment')
        self.area.addDock(self.P300_dock, 'above', self.emg_dock)
        # Add the layout to the dock
        self.P300_layout = pg.LayoutWidget()
        self.P300_dock.addWidget(self.P300_layout)

        self.p300_plot = self.instantiate_p300_plot()
        row=1; col=0; rowspan=1; colspan=2
        self.P300_layout.addWidget(self.p300_plot, row, col, rowspan, colspan)

        # # Start and stop button
        self.start_p300_button()
        self.stop_p300_button()
        # # Result label
        self.show_p300_result()

        self.timer_p300.timeout.connect(self.update_p300)

    def instantiate_p300_plot(self):
        p300_plot = pg.PlotWidget()
        p300_plot.setXRange(-2, 7)
        p300_plot.setYRange(-1, 5)
        p300_plot.hideAxis('bottom')
        p300_plot.hideAxis('left')
        return p300_plot

    def show_p300_result(self):
        result = QtGui.QLabel(f'Letter to look at: {"-G-"}')
        result.setFont(QtGui.QFont('SansSerif', pointSize=12))
        row=2; col=0; rowspan=1; colspan=1
        self.P300_layout.addWidget(result, row, col, rowspan, colspan)

    def update_p300(self):
        rand_row = randint(0, 5)
        rand_col = randint(0, 5)
        # clear the widget on the screen at every display to add a new batch
        self.p300_plot.clear()
        # Add all number to the plot
        for no, one_char in enumerate(self.p300_char):                         # TODO: Improve ALEXM instead of adding label and removing them all after each itteration just change the style of the label in black (see label for average and max)
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