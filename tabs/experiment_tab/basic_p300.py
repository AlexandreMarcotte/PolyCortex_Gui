# -- General Packages --
import pyqtgraph as pg
from PyQt5 import QtCore
from functools import partial
import numpy as np
# Paint rectangles
import random
from time import sleep
# -- My packages --
from app.colors import *
from .experiment import Experiment
from app.draw_rectangle import SquareItem


class BasicP300(Experiment):
    def __init__(self, area, dock_above, gv):
        super().__init__(timer_period=200)
        self.area = area
        self.dock_above = dock_above
        self.gv = gv

        exp_name = 'Basic P300'

        self.xs = (0, 10)
        self.ys = (0, 10)

        self.rand = 0

        self.plot_timer = QtCore.QTimer()
        self.create_dock(exp_name)
        # plot
        self.plot = self.create_plot(xs=self.xs, ys=self.ys)
        self.layout.addWidget(self.plot, 1, 0, 1, 2)

        self.plot_timer.timeout.connect(partial(
            self.create_rectangles_img, n_red_rect=30, n_green_rect=40))

        self.show_warning_text()

    def create_rectangles_img(self, n_red_rect, n_green_rect):
        self.rand = 1 - self.rand
        print(self.rand)
        # rand = random.randrange(2)
        if self.rand == 0:
            # Red
            self.clear_screen()
            p = SquareItem(
                    x=np.zeros(n_red_rect),
                    y=np.linspace(0, 10, n_red_rect),
                    w=10 * np.ones(n_red_rect),
                    h=0.35 * np.ones(n_red_rect),
                    color=p300_white)
            self.refresh()
            self.plot.addItem(p)
            self.gv.experiment_type = 1

        elif self.rand == 1:
            self.clear_screen()
            # sleep(0.1)

        else:
            print('Should not happen')
        """
        elif rand in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
            # Green
            self.clear_screen()
            p = SquareItem(
                x=np.linspace(0, 10, n_green_rect),
                y=np.zeros(n_green_rect),
                w=0.12 * np.ones(n_green_rect),
                h=10 * np.ones(n_green_rect),
                color=p300_green)
            self.refresh()  # So that the graph update and the rectangle are visible
            self.plot.addItem(p)
            sleep(0.05)
        """                                                                      # TODO: ALEXM: Try to find a cleaner way to update the graph

    def show_warning_text(self):
        self.warn_txt = pg.TextItem(anchor=(0, 0), fill=(0, 0, 0, 0))
        self.warn_html = f"""<div style="text-align: center">
                               <br><span style="color: {'#ff0000'};
                               font-size: 19pt;"><p>
                               {'''Warning this experiment has the potential 
                                   to induce SEIZURE'''}</p>
                                <p>{'''for people with Photosensitive EPILEPSY'''}</p>
                               </span></div>"""
        self.warn_txt.setHtml(self.warn_html)
        self.warn_txt.setPos(0, 10)
        self.plot.addItem(self.warn_txt)

    def clear_screen(self):
        self.plot.clear()
        self.refresh(delta_x=0.001)

    def refresh(self, delta_x=0.0):
        self.plot.setXRange(self.xs[0]+delta_x, self.xs[1])