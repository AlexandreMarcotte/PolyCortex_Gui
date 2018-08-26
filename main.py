# General packages
from collections import deque
import numpy as np
from time import time
# My packages
from visualisation_with_pyqt import OpenBciGui
# PyQt5
from PyQt5.QtWidgets import QApplication
import sys
# Dark theme
import qdarkstyle


def main():

    DEQUE_LEN = 1250
    N_CH = 8
    data_queue = [deque(np.zeros(DEQUE_LEN),
                  maxlen=DEQUE_LEN) for _ in range(N_CH)]  # One deque per channel initialize at 0
    t_queue = deque(np.zeros(DEQUE_LEN), maxlen=DEQUE_LEN)
    experiment_queue = deque(np.zeros(DEQUE_LEN), maxlen=DEQUE_LEN)
    experiment_type = [0]
    t_init = time()
    n_data_created = [1]

    # Start the multigraphes
    app = QApplication(sys.argv)
    # Apply dark theme
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # Create the Gui
    open_bci_gui = OpenBciGui(data_queue, t_queue, experiment_queue,
                              experiment_type, t_init, n_data_created)
    # start the main tread that contains all the timers
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


