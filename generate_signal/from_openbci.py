import threading
import logging
from time import sleep
# OpenBCI hardware module
import openbci_interface.open_bci_v3 as bci


class SampleDataFromOPENBCI(threading.Thread):
    def __init__(self, gv):
        super().__init__()
        self.gv = gv
        port = '/dev/ttyUSB0'  # if using Linux
        # (if encounter error: [Errno 13] could not open port /dev/ttyUSB0:
        #  Permission denied
        #  => see: https://askubuntu.com/questions/58119/changing-permissions-on-serial-port
        #    then restart your computer
        # port = 'COM3'  # if using Windows
        # port = '/dev/tty.OpenBCI-DN008VTF'  # If using MAC?
        # logging.basicConfig(filename="test.log", format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
        # logging.info('---------LOG START-------------')
        self.board = bci.OpenBCIBoard(
                port=port, scaled_output=False, log=True, filter_data=True)
        print("Board Instantiated")
        sleep(1)  # TODO: I changed it to 1 and it was 5 before see if there is a problem

    def run(self):
        self.board.start_streaming(self.gv.collect_data)
