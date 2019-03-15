from functools import partial
import os
# from save_to_file import WriteDataToFile
from app.colors import *
from app.pyqt_frequently_used import select_file

from PyQt5 import QtGui
# --My Packages--
from save.write_to_file import write_to_file


class DataSaver:
    def __init__(self, main_window, gv, layout, save_path=os.getcwd(),
                 saving_type='eeg save', pos=(0, 0), size=(1, 2),
                 save_file_button=True, choose_b_size=(1,1)):
        self.main_window = main_window
        self.layout = layout
        self.gv = gv
        self.save_path = save_path
        self.saving_type = saving_type
        self.pos = pos
        self.size = size
        self.save_file_button = save_file_button
        self.choose_b_size = choose_b_size

        self.create_layout()

    def create_layout(self):
        # Create text box to show or enter path to data file
        self.save_path_line_edit = QtGui.QLineEdit(self.save_path)
        self.layout.addWidget(self.save_path_line_edit, *self.pos, *self.size)
        self.init_choose_saving_file()
        if self.save_file_button:
            self.init_save_file_button()

    def init_choose_saving_file(self):
        """Create button to open date file"""
        open_file = QtGui.QPushButton('Choose save path')
        open_file.setStyleSheet(f'background-color: {grey3})')
        open_file.clicked.connect(partial(self.save_file_dialog))
        self.layout.addWidget(
                open_file, self.pos[0], self.pos[1]+1, *self.choose_b_size)

    def init_save_file_button(self):
        """Button to save all the current data that was generated"""
        save_cur_data_b = QtGui.QPushButton('Save data Now')
        save_cur_data_b.setStyleSheet(f'background-color: {grey3})')
        save_cur_data_b.clicked.connect(partial(write_to_file, self.gv))
        self.layout.addWidget(save_cur_data_b, self.pos[0]+1, self.pos[1], 1, 2)

    def save_file_dialog(self):
        f_name = select_file(self.main_window, open=False, f_extension='.csv')
        if f_name:
            if self.saving_type == 'eeg save':
                self.gv.save_path = f_name
            elif self.saving_type == 'curve 3D pos save':
                self.save_path = f_name
            self.save_path_line_edit.setText(f_name)

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

