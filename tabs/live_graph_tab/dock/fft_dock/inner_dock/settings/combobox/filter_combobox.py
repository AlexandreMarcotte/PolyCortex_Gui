from .setting_combobox import SettingCombobox


class FilterCombobox(SettingCombobox):
    def __init__(self, gv, plot_inner_dock, layout, name, pos, param,
                 editable=True, cols=1, tip=None):
        super().__init__(
            layout, name, pos, param, editable=editable, cols=cols, tip=tip)
        self.gv = gv

        self.plot_inner_dock = plot_inner_dock

        self.combo_to_filter = {
            'No filter': [], 'Bandpass': ['bandpass'],
            'Bandstop': ['bandstop'], 'Both': ['bandpass', 'bandstop']}

        self._connect(self.show_filter)

    def show_filter(self, txt):
        self.gv.filter_to_use = self.combo_to_filter[txt]


