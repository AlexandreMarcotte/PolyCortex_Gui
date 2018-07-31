# General packages
from collections import deque
import numpy as np
import threading
from time import time
# My packages
from generated_signal import CreateData, CreateDataFromFile
from visualisation_with_pyqt import MultiChannelsPyQtGraph, App
from save_to_file import WriteDataToFile
# PyQt5
from PyQt5.QtWidgets import QApplication
import sys
# Dark theme
import qdarkstyle


def main():
    DEQUE_LEN = 500
    N_Ch = 8
    data_queue = [deque(np.zeros(DEQUE_LEN),
                  maxlen=DEQUE_LEN) for _ in range(N_Ch)]  # One deque per channel initialize at 0
    t_queue = deque(np.zeros(DEQUE_LEN), maxlen=DEQUE_LEN)
    t_init = time()

    n_data_created = [1]
    lock = threading.Lock()

    # Create fake data for test case
    create_data = CreateData(data_queue, t_queue, t_init, n_data_created)
    create_data.start()
    # create_data = CreateDataFromFile(data_queue)
    # create_data.start()

    # write data to file:
    # write_data_to_file = WriteDataToFile(data_queue, n_data_created, lock)
    # write_data_to_file.start()

    # Start the multigraphes
    app = QApplication(sys.argv)
    # Dark theme
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # multi_ch = MultiChannelsPyQtGraph(data_queue, n_data_created)
    # multi_ch.start_timer()
    multi_ch = App(data_queue, t_queue, t_init, n_data_created)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
