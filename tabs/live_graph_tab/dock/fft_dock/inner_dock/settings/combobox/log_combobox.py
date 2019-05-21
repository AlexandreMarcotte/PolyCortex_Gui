from .setting_combobox import SettingCombobox


class LogCombobox(SettingCombobox):
    def __init__(self, plot_inner_dock, layout, name, pos, param, editable=True,
                 cols=1, tip=None):
        super().__init__(
            layout, name, pos, param, editable=editable, cols=cols, tip=tip)

        self.plot_inner_dock = plot_inner_dock

        self._connect(self._log_axis)

    def _log_axis(self, txt):
        self.plot_inner_dock.plot.setLogMode(y=eval(txt))


