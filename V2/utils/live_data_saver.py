import threading
from time import sleep
import numpy as np


class LiveDataSaver(threading.Thread):
    def __init__(self, save_path, data_queue, t_queue, experiment_queue,
                 n_val_created, lock):
        super().__init__()
        self.save_path = save_path
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
                with open(self.save_path, 'a') as f:
                    # Create the proper dimension for the concatenation
                    t_queue = np.array(self.t_queue)[None, :]
                    experiment_queue = np.array(self.experiment_queue)[None, :]
                    save_val = np.concatenate((self.data_queue, t_queue,
                                               experiment_queue))
                    np.savetxt(f, np.transpose(save_val), delimiter=',')
                self.lock.release()
#


# KEEP THIS CODE (Was used to write data to file in live while collecting it
# BUT as the data is quite small I prefer to only dump it into file at the end
# end of the experiment)


