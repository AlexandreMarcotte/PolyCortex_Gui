from .setting_combobox import SettingCombobox
from functools import partial
import re


class ScaleAxisCombobox(SettingCombobox):
    def __init__(self, plot_inner_dock, layout, name, pos, param, editable=True,
                 cols=1, tip=None, axis_name='x'):
        super().__init__(
                layout, name, pos, param, editable=editable, cols=cols, tip=tip)
        self.plot_inner_dock = plot_inner_dock

        self._connect(axis_name)

    def _connect(self, axis_name):
        self.activated[str].connect(partial(self.scale_axis, axis_name=axis_name))

    def scale_axis(self, txt, axis_name):
        try:
            if txt == 'Auto':
                self.plot_inner_dock.plot.enableAutoRange()
            else:
                r = int(re.search(r'\d+', txt).group())
                if axis_name == 'x':
                    self.plot_inner_dock.plot.setXRange(0, r)
                elif axis_name == 'y':
                    self.plot_inner_dock.plot.setYRange(0, r)
        except AttributeError:
            print("This is an invalid value")

