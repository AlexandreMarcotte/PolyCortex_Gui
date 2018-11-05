import threading
import numpy as np
from time import sleep
import atexit
from functools import partial
from datetime import datetime
# from save_to_file import WriteDataToFile

from PyQt5 import QtGui
from PyQt5.QtWidgets import *


class DataSaver:
    def __init__(self, main_window, layout):
        self.main_window = main_window
        self.layout = layout
        init_time = datetime.now()
        self.save_path = f'./csv_saved_files/2exp_pinch_close_{init_time}.csv'

    def save_data_to_file(self):
        # Create text box to show or enter path to data file
        self.save_path_line_edit = QtGui.QLineEdit(self.save_path)
        self.layout.addWidget(self.save_path_line_edit, 0, 0, 1, 2)
        # Create button to open date file
        open_file = QtGui.QPushButton('Choose saving directory')
        open_file.clicked.connect(partial(self.save_file_dialog))
        self.layout.addWidget(open_file, 1, 0, 1, 1)
        # Button to save all the current data that was generated
        self.save_cur_data_b = QtGui.QPushButton('Save data Now')
        self.layout.addWidget(self.save_cur_data_b, 1, 1, 1, 1)


    def save_file_dialog(self):
        # From: https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            self.main_window, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.save_path = file_name
            self.data_path_line_edit.setText(self.save_path)


    def init_saving(self):  # KEEP THIS PORTION OF THE CODE (COMMENTED SO THAT IT DOESNT ALWAYS SAVE)
        pass
        # # write data to file:
        # self.write_data_to_file = WriteDataToFile(
        #     self.save_path, self.gv.data_queue, self.gv.t_queue,
        #     self.gv.experiment_queue,self.gv.n_data_created, self.lock)
        # # self.write_data_to_file.start()
        # self.write_data_to_file.at_exit_job()

    def write_to_file(self):
        print(f'Save data to file...')

        with open(self.save_path, 'w') as f:
            # Make sure all the queue in self.gv.all_data are the same length
            all_len = [len(d) for d in self.gv.all_data] + [len(self.gv.all_t)] \
                      + [len(self.gv.all_experiment_val)]
            print(all_len)
            min_len = min(all_len)
            # Remove extra data
            for i in range(len(self.gv.all_data)):
                if len(self.gv.all_data[i]) > min_len:
                    print('plus grand')
                    self.gv.all_data[i].pop()

            if len(self.gv.all_t) > min_len:
                self.gv.all_t.pop()

            if len(self.gv.all_experiment_val) > min_len:
                self.all_experiment_data.pop()

            # Create the proper dimension for the concatenation
            t_queue = np.array(self.gv.all_t)[None, :]
            experiment_queue = np.array(self.gv.all_experiment_val)[None, :]

            # Concatenate
            save_val = np.concatenate((self.gv.all_data, t_queue,
                                       experiment_queue))
            # Save
            np.savetxt(f, np.transpose(save_val), delimiter=',')
        
        
# class WriteDataToFile(threading.Thread):
#     def __init__(self, save_path, data_queue, t_queue, experiment_queue, 
#                  n_val_created, lock):
#         super(WriteDataToFile, self).__init__()
#         self.save_path = save_path
#         self.n_val_created = n_val_created
#         self.data_queue = data_queue
#         self.experiment_queue = experiment_queue
#         self.t_queue = t_queue
#         self.N_DATA = len(self.data_queue[0])
#         self.lock = lock
# 
#     def run(self):
#         self.write_to_file()
# 
#     def write_to_file(self):
#         while 1:
#             sleep(0.001)
#             if self.n_val_created[0] % self.N_DATA == 0:
#                 self.lock.acquire()
#                 with open(self.save_path, 'a') as f:
#                     # Create the proper dimension for the concatenation
#                     t_queue = np.array(self.t_queue)[None, :]
#                     experiment_queue = np.array(self.experiment_queue)[None, :]
#                     save_val = np.concatenate((self.data_queue, t_queue,
#                                                experiment_queue))
#                     np.savetxt(f, np.transpose(save_val), delimiter=',')
#                 self.lock.release()
                
                
        
# KEEP THIS CODE

