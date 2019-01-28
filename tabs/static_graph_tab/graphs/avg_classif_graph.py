# -- General Packages --
import numpy as np
import os
from sklearn.externals import joblib
import pyqtgraph as pg
from PyQt5.QtWidgets import *
# -- My packages --
from ... static_graph_tab.graphs.graph import Graph
from data_processing_pipeline.calcul_fft import FreqCalculator


class AvgClassifGraph(Graph):
    def __init__(self):
        super().__init__()
        
        self.curve = None 
        self.classif_region_curve = None
        self.combo_box_curve = None
        
        self.num = pg.TextItem(anchor=(0, 0), fill=(0, 0, 0, 0))
        self.classif_type = 0

        # os.chdir('..')
        # project_base_path = os.getcwd()
        avg_emg_path = 'machine_learning/avg_emg_class_type.npy'
        self.avg_emg_class_type = np.load(os.path.join(os.getcwd(), avg_emg_path))
        self.classified_data = None
        self.combo_classif = self.add_classif_num_combobox()

    def update_pos_and_avg_graph(self, classif_region_pos):
        self.add_classif_class_number()
        try:
            classified_type = self.classified_data[int(classif_region_pos)]
            self.num.setHtml(str(classified_type))
            data = self.avg_emg_class_type[classified_type]
            # if data.any() and t.any() and not np.isnan(np.sum(data)):
            #     freq_calculator = FreqCalculator(
            #         remove_first_data=2, data_q=data, t_q=t)
            #     freq_range = freq_calculator.get_freq_range()
            #     fft = freq_calculator.fft()
            data = data.reshape((data.shape[0],))
            self.curve.setData(data)
        except IndexError as e:
            print(e)
            
    def update_avg_graph_from_combo_box(self, combo_box_value):
        data = self.avg_emg_class_type[int(combo_box_value)]
        # if data.any() and not np.isnan(np.sum(data)):
        #     freq_calculator = FreqCalculator(
        #         remove_first_data=2, data_q=data, t_q=t)
        #     freq_range = freq_calculator.get_freq_range()
        #     fft = freq_calculator.fft()
        #     self.combo_box_curve.setData(freq_range, fft)
        self.combo_box_curve.setData(data)

    def update_classif_region_plot(self, data):
        # if data.any() and not np.isnan(np.sum(data)):
        #     freq_calculator = FreqCalculator(
        #         remove_first_data=2, data_q=data, t_q=t)
        #     freq_range = freq_calculator.get_freq_range()
        #     fft = freq_calculator.fft()
        #     self.classif_region_curve.setData(freq_range, fft)
        self.classif_region_curve.setData(data)

    def get_fft(self):
        pass

    def add_classif_class_number(self):
        html = f'{self.classif_type}' 
        self.num.setHtml(html)
        self.num.setPos(0, 0.5)
        self.plot.addItem(self.num)

    def add_classif_num_combobox(self):
        N_CLASSIF_TYPE = len(self.avg_emg_class_type)
        print('N_CLASSIF', N_CLASSIF_TYPE)
        combo_classif = QComboBox()
        for i in range(N_CLASSIF_TYPE): 
            combo_classif.addItem(str(i))
        return combo_classif
            
