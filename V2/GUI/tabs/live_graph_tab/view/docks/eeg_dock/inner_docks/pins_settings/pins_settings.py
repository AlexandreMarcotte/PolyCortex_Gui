from PyQt5.QtWidgets import QComboBox


class PinSettings:
    def __init__(self):

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
        self.comboboxes = dict()

    def add_pin_settings_to_layout(self, layout):
        for i, (setting_name, settings) in enumerate(self.settings.items()):
            cb = QComboBox()
            self.comboboxes[setting_name] = cb
            # Save for further uses
            cb.setStyleSheet(
                'QComboBox'
                '{background-color: rgba(170, 170, 170, 200);'
                'color:white;'
                'selection-background-color: darkblue;'
                'border: 2px solid rgba(220, 220, 220, 100);}'
                'QListView{color:red; background-color:black}')
            for setting in settings:
                cb.addItem(setting)
            layout.addWidget(cb, 0, i+1)

    def hide_pins_settings(self):
         # itterate over all cb
        for cb in self.comboboxes.values():
            cb.hide()

    def show_pins_settings(self):
        for cb in self.comboboxes.values():
            cb.show()








    """
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
    """
