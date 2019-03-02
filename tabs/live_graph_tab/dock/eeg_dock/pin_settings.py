# -General Packages-
from functools import partial
from PyQt5.QtWidgets import *
from time import sleep
#-My Packages-
from app.pyqt_frequently_used import create_param_combobox
from app.pyqt_frequently_used import create_gr


class PinSettings:
    def __init__(self, eeg_plot_creator, gv, layout, ch):
        self.eeg_plot_creator = eeg_plot_creator
        self.gv = gv
        self.ch = ch

        self.command = {
                'Ch': 0, 'Power down': 0, 'PGA Gain': 0, 'Input Type': 0,
                'Biais': 0, 'SRB2': 0, 'SRB1': 0
                }

        self.settings = {
                'PGA Gain':
                        {'x1': 0, 'x2': 1, 'x4': 2, 'x6': 3,
                         'x8': 4, 'x12': 5, 'x24': 6},
                'Input Type':
                        {'Normal': 0, 'shorted': 1, 'biais meas': 2,
                         'mvdd': 3, 'temp': 4, 'testsig': 5,
                         'biais drp': 6, 'biais drn': 7},
                'Biais':
                        {"Don't include": 0, 'Include': 1},
                'SRB2':
                        {'No': 0, 'Yes': 1},
                'SRB1':
                        {'Off': 0, 'On': 1}
                }
        self.add_pin_settings_to_layout(layout)

    def add_pin_settings_to_layout(self, layout):
        self.gr, self.ch_layout = create_gr()
        for i, (s_name, s) in enumerate(self.settings.items()):
            create_param_combobox(
                    self.ch_layout, None, (i%5, i//5), s,
                    conn_func=partial(self.change_hardware_settings, s_name),
                    editable=False, tip=s_name)
        layout.addWidget(self.gr, self.ch, 0)

    def change_hardware_settings(self, setting_name, opt_selected):
        if setting_name == 'PGA Gain':
            # Remove the x in the string of the gain
            gain = opt_selected[1:]
            self.gv.gain = int(gain)
            # Calcul the new scalling factor
            self.gv.scaling_factor[self.ch] = 4.5 / (self.gv.gain * (2**(23-1)))

        sett_command = self.settings[setting_name][opt_selected]
        # Create the setting values
        self.command['Ch'] = self.ch + 1
        self.command[setting_name] = sett_command
        # Start the setting string
        byte_settings = 'x'
        for key, val in self.command.items():
            byte_settings += str(val)
        # End the settings string
        byte_settings += 'X'
        try:
            for b in byte_settings:
                self.eeg_plot_creator.stream_source.board.ser_write(b.encode())
                sleep(0.01)
            print('Send settings to board: ', byte_settings)
        except AttributeError as e:
            print('You are not connected to the OpenBCI board')
