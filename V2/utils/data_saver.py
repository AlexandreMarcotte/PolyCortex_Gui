from PyQt5.QtWidgets import *
# --My Packages--
from V2.utils.colors import Color
from V2.utils.btn import Btn
from save.write_to_file import write_to_file
from V2.general_settings import GeneralSettings
from V2.utils.select_file import select_file
from V2.utils.write_to_file import write_to_file


class DataSaver:
    def __init__(
            self, layout,
            save_path='/home/alex/Documents/CODING/2019/PolyCortex_Gui/V2/pipeline/signal_streamer/from_file/experiment_csv',
            pos=(0, 0)):

        self.layout = layout

        self.save_path = save_path
        self.pos = pos

        self.save_path_line_edit = self._init_save_path_line_edit(save_path)

        self.choose_save_path_btn = self._init_btn(
            'Save path', pos=(pos[0], pos[1]+1))
        self._connect_choose_save_path_btn()

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

    def _connect_choose_save_path_btn(self):
        self.choose_save_path_btn.clicked.connect(self._set_save_path)

    # def _connect_save_btn(self):
    #     self.save_data_now_btn.clicked.connect(write_to_file(None))

    def _set_save_path(self):
        save_path = select_file(GeneralSettings.main_window, open=True)
        if save_path:
            self.save_path = save_path

    def connect_signal_to_save(self, signal):
        self.signal = signal







    # def init_saving(self):                                                   # KEEP THIS PORTION OF THE CODE (COMMENTED SO THAT IT DOESNT ALWAYS SAVE)
    #     write data to file:
        # self.write_data_to_file = WriteDataToFile(
        #     self.gv.save_path, self.gv.data_queue, self.gv.t_queue,
        #     self.gv.experiment_queue,self.gv.n_data_created, self.lock)
        # self.write_data_to_file.start()
        # self.write_data_to_file.at_exit_job()


    # def save_file_dialog(self):
    #     f_name = select_file(self.main_window, open=False, f_extension='.csv')
    #     if f_name:
    #         if self.saving_type == 'eeg save':
    #             self.gv.save_path = f_name
    #         elif self.saving_type == 'curve 3D pos save':
    #             self.save_path = f_name
    #         self.save_path_line_edit.setText(f_name)



