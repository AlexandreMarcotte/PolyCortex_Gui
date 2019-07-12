from PyQt5 import QtCore, QtGui
from time import sleep
# --My Packages--
from V2.utils.btn import Btn
from V2.utils.colors import *
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock


class WriteHardwareDock(InnerDock):
    def __init__(self, external_layout=None):
        super().__init__(
            name='Write hardware', toggle_btn=True, b_checked=False,
            set_scroll=False, external_layout=external_layout)

        self._add_line_edit()
        self._add_btn()

    def _add_line_edit(self):
        self.l_e = QtGui.QLineEdit('x1040000X')
        self.inner_layout.addWidget(self.l_e, 0, 0, 1, 3)

    def _add_btn(self):
        self.btn = Btn(name='Write serial', color=grey3, txt_color=black)
        self.inner_layout.addWidget(self.btn, 0, 3)

    def send_byte_to_hardware(self):
        print('Send: ', f'{self.l_e.text()}')
        byte_settings = self.l_e.text()
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
