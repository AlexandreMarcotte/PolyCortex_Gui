# -- General Packages --
import pyqtgraph as pg
import numpy as np
# -- My Packages --
from V2.GUI.tabs.experiment_tab.docks.experiment import Experiment


class BinaryExperimentDock(Experiment):
    def __init__(self, area, dock_above=None):
        super().__init__(area, name='Binary', dock_above=dock_above,
                         timer_period=5)

        self._actions = ['PINCH', 'CLENCH', 'TAP']
        self._len_actions = len(self._actions)
        self._len_list = 50
        self._index = 0
        self._action_index = 0

        self.plot = self.create_plot()
        self._pg_layout.addWidget(self.plot, 1, 0, 1, 2)
        self.create_experiment()

    def _create_vertical_curve(self):
        x = np.zeros(self._len_list)
        y = np.arange(0, self._len_list)
        curve = self.plot.plot(x, y)
        return curve

    def _create_horizontal_curve(self):
        x2 = np.arange(-self._len_list//2, self._len_list//2)
        y2 = self._len_list // 2 * np.ones(self._len_list)
        self.plot.plot(x2, y2)

    def _create_curve_pt(self, curve):
        curve_pt = pg.CurvePoint(curve)
        self.plot.addItem(curve_pt)
        arrow = pg.ArrowItem(angle=90)
        arrow.setParentItem(curve_pt)
        return curve_pt

    def _create_txt(self, curve_pt):
        txt = pg.TextItem('BEFORE action', anchor=(0.5, -1.0))
        txt.setParentItem(curve_pt)
        return txt

    def create_experiment(self):
        self._create_horizontal_curve()
        curve = self._create_vertical_curve()
        self._curve_pt = self._create_curve_pt(curve)
        self._txt = self._create_txt(self._curve_pt)

    def update(self):
        self._index = (self._index + 1) % self._len_list
        self._curve_pt.setPos(self._index/(self._len_list-1))
        if self._index == 0:
            self._txt.setText(f'{self._actions[self._action_index]} action')
            self._action_index = (self._action_index + 1) % self._len_actions
        if self._index == self._len_list//2:
            # Toggle the experiment event
            self.signal_collector.experiment_event = 1
            self._txt.setText('NOW')




