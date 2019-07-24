import os

from PyQt5.QtWidgets import *
# --My Packages--
from V2.utils.colors import Color
from V2.utils.btn import Btn
from save.write_to_file import write_to_file


class DataSaver:
    def __init__(self, layout, save_path=os.getcwd(), pos=(0, 0)):

        self.layout = layout
        self.pos = pos

        self.save_path_line_edit = self._init_save_path_line_edit(save_path)

        self.chose_save_path_btn = self._init_btn(
            'Save path', pos=(pos[0], pos[1]+1))

        self.save_data_now_btn = self._init_btn(
            'Save data now', pos=(self.pos[0]+1, self.pos[1]), size=(1, 2))

    def _init_save_path_line_edit(self, save_path):
        """Create text box to show or enter path to data file"""
        le = QLineEdit(save_path)
        self.layout.addWidget(le, *self.pos, 1, 1)
        return le

    def _init_btn(self, name, pos, size=(1, 1)):
        b = Btn(name=name, color=Color.grey3, txt_color=Color.black)
        self.layout.addWidget(b, *pos, *size)
        return b

    # def save_file_dialog(self):
    #     f_name = select_file(self.main_window, open=False, f_extension='.csv')
    #     if f_name:
    #         if self.saving_type == 'eeg save':
    #             self.gv.save_path = f_name
    #         elif self.saving_type == 'curve 3D pos save':
    #             self.save_path = f_name
    #         self.save_path_line_edit.setText(f_name)

















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
