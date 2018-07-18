# General packages
from collections import deque
import numpy as np
import threading
# My packages
from generated_signal import CreateData, CreateDataFromFile
from visualisation_with_pyqt import MultiChannelsPyQtGraph
from save_to_file import WriteDataToFile

def main():
    DEQUE_LEN = 200
    N_Ch = 8
    data_queue = [deque(np.zeros(DEQUE_LEN),
                  maxlen=DEQUE_LEN) for _ in range(N_Ch)]  # One deque per channel initialize at 0
    n_data_created = [1]
    lock = threading.Lock()

    # Create fake data for test case
    create_data = CreateData(data_queue, n_data_created)
    create_data.start()
    # create_data = CreateDataFromFile(data_queue)
    # create_data.start()

    # write data to file:
    write_data_to_file = WriteDataToFile(data_queue, n_data_created, lock)
    write_data_to_file.start()

    # Start the multigraphes
    multich_plot = MultiChannelsPyQtGraph(data_queue, n_data_created)
    multich_plot.exec_plot()


if __name__ == '__main__':
    main()
