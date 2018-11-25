import threading
import logging
# OpenBCI hardware module
import openbci_interface.open_bci_v3 as bci

from time import sleep
from time import time


def stream_data_from_OpenBCI(gv):
    port = '/dev/ttyUSB0'  # if using Linux
    # (if encounter error: [Errno 13] could not open port /dev/ttyUSB0: Permission denied => see: https://askubuntu.com/questions/58119/changing-permissions-on-serial-port   then restart your computer
    # port = 'COM3'  # if using Windows
    # port = '/dev/tty.OpenBCI-DN008VTF'  # If using MAC?
    logging.basicConfig(filename="test.log", format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
    logging.info('---------LOG START-------------')
    board = bci.OpenBCIBoard(port=port, scaled_output=False, log=True)
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

    def add_data_to_queue(self, sample):
        for ch, one_sample in enumerate(sample.channel_data):
            self.gv.data_queue[ch].append(one_sample)
            self.gv.all_data[ch].append(one_sample)
        self.gv.n_data_created[0] += 1
        # Time
        current_time = time() - self.gv.t_init
        self.gv.t_queue.append(current_time)
        self.gv.all_t.append(current_time)
        # Add experiment type values
        if self.gv.experiment_type[0] != 0:
            typ = self.gv.experiment_type[0]
            self.gv.experiment_queue.append(typ)
            self.gv.all_experiment_val.append(typ)
            self.gv.experiment_type[0] = 0
        else:
            self.gv.experiment_queue.append(0)
            self.gv.all_experiment_val.append(0)