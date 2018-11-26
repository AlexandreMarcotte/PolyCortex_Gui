import threading
import logging
from time import sleep
# OpenBCI hardware module
import openbci_interface.open_bci_v3 as bci


def stream_data_from_OpenBCI(gv):
    port = '/dev/ttyUSB0'  # if using Linux
    # (if encounter error: [Errno 13] could not open port /dev/ttyUSB0: Permission denied => see: https://askubuntu.com/questions/58119/changing-permissions-on-serial-port   then restart your computer
    # port = 'COM3'  # if using Windows
    # port = '/dev/tty.OpenBCI-DN008VTF'  # If using MAC?
    logging.basicConfig(filename="test.log", format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
    logging.info('---------LOG START-------------')
    board = bci.OpenBCIBoard(port=port, scaled_output=False, log=True)
    board.enable_filters()
    print("Board Instantiated")
    sleep(5)

    OpenBCI_sampler = SampleDataFromOPENBCI(board, gv)
    OpenBCI_sampler.start()

    return board


class SampleDataFromOPENBCI(threading.Thread):
    def __init__(self, board, gv):
        super().__init__()
        self.board = board
        self.gv = gv

    def run(self):
        # Previously and Working
        self.board.start_streaming(self.gv.collect_data)