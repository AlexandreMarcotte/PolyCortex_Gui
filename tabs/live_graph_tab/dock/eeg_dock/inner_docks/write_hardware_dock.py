from tabs.live_graph_tab.dock.inner_dock import InnerDock
from PyQt5 import QtCore, QtGui
from app.activation_b import btn
from time import sleep


class WriteHardwareDock:
    def __init__(self, main_eeg_dock):
        self.main_eeg_dock = main_eeg_dock
        self.create_layout()

    def create_layout(self):
        write_hardware_d = InnerDock(
            self.main_eeg_dock.layout, 'Write to hardware', b_pos=(0, 4),
            toggle_button=True, size=(1, 1), b_checked=True)
        self.write_hardware_l_e = QtGui.QLineEdit('x1040000X')
        write_hardware_d.layout.addWidget(self.write_hardware_l_e)
        btn('Write serial', write_hardware_d.layout,
            func_conn=self.send_byte_to_hardware, pos=(0, 1))
        self.main_eeg_dock.dock_area.addDock(write_hardware_d.dock)
        # write_hardware_d.dock.hide()

    def send_byte_to_hardware(self):
        print('Send: ', f'{self.write_hardware_l_e.text()}')
        byte_settings = self.write_hardware_l_e.text()
        # self.stream_source.board.ser_write(byte_settings)
        try:
            for b in byte_settings:
                self.main_eeg_dock.stream_source.board.ser_write(b.encode())
                sleep(0.01)
            self.write_hardware_l_e.setText('')
        except AttributeError as e:
            # Remove the command sent
            print('You are not connected to the OpenBCI board')
            self.write_hardware_l_e.setText('')

