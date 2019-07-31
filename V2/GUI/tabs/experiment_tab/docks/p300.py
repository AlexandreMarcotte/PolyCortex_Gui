# -- General packages --
from PyQt5 import QtGui, QtCore

import pyqtgraph as pg

from random import randint
# -- My packages --
from V2.GUI.tabs.experiment_tab.docks.experiment import Experiment


class P300Dock(Experiment):
    def __init__(self, area, dock_above):
        super().__init__(
            area, name='P300', dock_above=dock_above, timer_period=50)

        self.p300_char = ['A', 'B', 'C', 'D', 'E', 'F',
                          'G', 'H', 'I', 'J', 'K', 'L',
                          'M', 'N', 'O', 'P', 'Q', 'R',
                          'S', 'T', 'U', 'V', 'W', 'X',
                          'Y', 'Z', '1', '2', '3', '4',
                          '5', '6', '7', '8', '9', '0']
        self.show_p300 = True
        # Plot
        self.plot = self.create_plot()
        self._pg_layout.addWidget(self.plot, 1, 0, 1, 2)
        # Result label
        self._show_p300_result()

    def _show_p300_result(self):
        result = QtGui.QLabel(f'Letter to look at:     -G-    ')
        result.setFont(QtGui.QFont('SansSerif', pointSize=15))
        self._pg_layout.addWidget(result, 2, 0)

    def update(self):
        rand_row = randint(0, 5)
        rand_col = randint(0, 5)
        # clear the widget on the screen at every display to add a new batch
        self.plot.clear()
        # Add all number to the plot
        for no, one_char in enumerate(self.p300_char):  # TODO: Improve ALEXM instead of adding label and removing them all after each itteration just change the style of the label in black (see label for average and max)
            col = no % 6
            row = no // 6
            # Change the color on the row and column selected from the random
            # # Selected row
            if rand_col == col or rand_row == row:
                char_color = '#111'
            else:
                char_color = '#888'

            char = pg.TextItem(fill=(0, 0, 0), anchor=(0.5, 0))
            html = f"""<span style="color: {char_color};
                       font-size: 56pt; ">
                       {one_char}"""
            char.setHtml(html)

            char.setPos(col, row)
            self.plot.addItem(char)
