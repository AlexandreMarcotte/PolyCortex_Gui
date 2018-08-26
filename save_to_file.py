import threading
import numpy as np
from time import sleep

class WriteDataToFile(threading.Thread):
    def __init__(self, data_queue, t_queue, experiment_queue, n_val_created,
                 lock):
        super(WriteDataToFile, self).__init__()
        self.n_val_created = n_val_created
        self.data_queue = data_queue
        self.experiment_queue = experiment_queue
        self.t_queue = t_queue
        self.N_DATA = len(self.data_queue[0])
        self.lock = lock

    def run(self):
        self.write_to_file()

    def write_to_file(self):
        while 1:
            sleep(0.001)
            if self.n_val_created[0] % self.N_DATA == 0:
                self.lock.acquire()
                with open('csv_eeg_data.csv', 'a') as f:
                    # Create the proper dimension for the concatenation
                    t_queue = np.array(self.t_queue)[None, :]
                    experiment_queue = np.array(self.experiment_queue)[None, :]
                    save_val = np.concatenate((self.data_queue, t_queue,
                                               experiment_queue))
                    np.savetxt(f, np.transpose(save_val), delimiter=',')
                self.lock.release()


