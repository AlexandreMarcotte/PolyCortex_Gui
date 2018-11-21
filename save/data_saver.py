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
    def __init__(self, main_window, layout, gv):
        self.main_window = main_window
        self.layout = layout
        self.gv = gv
        init_time = datetime.now()
        self.gv.save_path = f'./experiment_csv/2exp_pinch_close_{init_time}.csv'

    def save_data_to_file(self):
        # Create text box to show or enter path to data file
        self.save_path_line_edit = QtGui.QLineEdit(self.gv.save_path)
        self.layout.addWidget(self.save_path_line_edit, 0, 0, 1, 2)
        # Create button to open date file
        open_file = QtGui.QPushButton('Choose saving directory')
        open_file.setStyleSheet("background-color: rgba(200, 200, 200, 0.6)")
        open_file.clicked.connect(partial(self.save_file_dialog))
        self.layout.addWidget(open_file, 1, 0)
        # Button to save all the current data that was generated
        save_cur_data_b = QtGui.QPushButton('Save data Now')
        save_cur_data_b.setStyleSheet("background-color: rgba(200, 200, 200, 0.6)")
        self.layout.addWidget(save_cur_data_b, 1, 1)

    def save_file_dialog(self):
        # From: https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        f_name, _ = QFileDialog.getSaveFileName(
            self.main_window, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;Text Files (*.txt)", options=options)
        if f_name:
            self.gv.save_path = f_name
            self.data_path_line_edit.setText(self.gv.save_path)

    # def init_saving(self):                                                   # KEEP THIS PORTION OF THE CODE (COMMENTED SO THAT IT DOESNT ALWAYS SAVE)
    #     # write data to file:
    #     self.write_data_to_file = WriteDataToFile(
    #         self.gv.save_path, self.gv.data_queue, self.gv.t_queue,
    #         self.gv.experiment_queue,self.gv.n_data_created, self.lock)
    #     # self.write_data_to_file.start()
    #     self.write_data_to_file.at_exit_job()
        
        
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
                
                
        
# KEEP THIS CODE (Was used to write data to file in live while collecting it
# BUT as the data is quite small I prefer to only dump it into file at the end
# end of the experiment)

