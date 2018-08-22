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
    t_init = time()
    n_data_created = [1]

    # Start the multigraphes
    app = QApplication(sys.argv)
    # Dark theme
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    open_bci_gui = OpenBciGui(data_queue, t_queue, t_init, n_data_created)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()