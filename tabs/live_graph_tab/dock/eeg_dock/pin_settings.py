from app.pyqt_frequently_used import create_param_combobox


class PinSettings:
    def __init__(self, gv, layout, ch):
        self.gv = gv
        self.ch = ch

        self.settings_name = ['PGA Gain', 'Input Type', 'Bias', 'SRB2', 'SRB1']
        self.settings = [
            ['x24', 'x8'],
            ['Normal', 'Abnormal'],
            ["Don't include", 'Include'],
            ['Off', 'On'],
            ['No', 'Yes']]
        self.add_pin_settings_to_layout(layout)

    def add_pin_settings_to_layout(self, layout):
        for i, (s, s_name) in enumerate(zip(
                self.settings, self.settings_name)):
            create_param_combobox(
                layout, None, (self.ch, i), s,
                conn_func=self.change_hardware_settings,
                editable=False, tip=s_name)

    def change_hardware_settings(self):
        print('change the hardware settings for the pin number ', self.ch)
