import threading
import logging
from time import sleep
# --My Packages--
# OpenBCI hardware module
from . import open_bci_v3 as bci
from ..signal_collector import SignalCollector


class SampleDataFromOpenBci(threading.Thread):
    def __init__(self, signal_collector: SignalCollector):
        super().__init__()

        self.signal_collector = signal_collector

        port = '/dev/ttyUSB0'  # if using Linux

        # (if encounter error: [Errno 13] could not open port /dev/ttyUSB0:
        #  Permission denied
        #  => see: https://askubuntu.com/questions/58119/changing-permissions-on-serial-port
        #    then restart your computer
        # port = 'COM3'  # if using Windows
        # port = '/dev/tty.OpenBCI-DN008VTF'  # If using MAC?
        # logging.basicConfig(filename="test.log", format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
        # logging.info('---------LOG START-------------')

        # If you cannot access the port, you need to add yourself to the dialout group
        # https://askubuntu.com/questions/210177/serial-port-terminal-cannot-open-dev-ttys0-permission-denied
        self.board = bci.OpenBCIBoard(
                port=port, scaled_output=False, log=True, filter_data=True)
        print('Board Instantiated')
        sleep(5)  # TODO: I changed it to 1 and it was 5 before see if there is a problem

    def run(self):
        self.board.start_streaming(self.signal_collector.fill_signal_queue)