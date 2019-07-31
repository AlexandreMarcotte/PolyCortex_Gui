from numpy import genfromtxt
import os
# --My packages--
from V2.pipeline.pipeline import Pipeline
from V2.general_settings import GeneralSettings


class Model:
    def __init__(self):
        self.N_CH = 8

        self.pipeline = Pipeline()

        self.board = None

        self.static_data = None

    def load_data(self):
        print('load data')
        base_path = os.getcwd()
        file_name = os.path.join(base_path, GeneralSettings.file.stream_path)
        data = genfromtxt(file_name, delimiter=',')
        return data
