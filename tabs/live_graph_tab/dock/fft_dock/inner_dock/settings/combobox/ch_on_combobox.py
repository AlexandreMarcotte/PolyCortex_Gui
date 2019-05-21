from .setting_combobox import SettingCombobox


class ChOnCombobox(SettingCombobox):
    def __init__(self, gv, plot_inner_dock, layout, name, pos, param,
                 editable=True, cols=1, tip=None):
        super().__init__(
                layout, name, pos, param, editable=editable, cols=cols, tip=tip)
        self.gv = gv

        self.plot_inner_dock = plot_inner_dock

        self._connect(self.ch_on_off)

    def ch_on_off(self, ch):
        if ch == 'all':
            # Create a list full of every ch number
            self.plot_inner_dock.ch_to_show = list(range(self.gv.N_CH))
        else:
            # Keep the numeric value of the combobox
            self.plot_inner_dock.ch_to_show = [int(ch[3:]) - 1]  # TODO: Use a re instead
        self.clear_curves()

    def clear_curves(self):
        for c in self.plot_inner_dock.freq_curves:
            c.clear()
