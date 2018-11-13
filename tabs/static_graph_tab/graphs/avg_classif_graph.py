# -- General Packages --
import numpy as np
import os
from sklearn.externals import joblib
import pyqtgraph as pg
# -- My packages --
from ... static_graph_tab.graphs.graph import Graph

class AvgClassifGraph(Graph):
    def __init__(self):
        super().__init__()
        
        self.curve = None 
        self.classif_region_curve = None
        
        self.num = pg.TextItem(anchor=(0, 0), fill=(0, 0, 0, 0))
        self.classif_type = 0
        avg_emg_path = 'tabs/static_graph_tab/avg_emg_class_type.npy'
        self.avg_emg_class_type = np.load(os.path.join(os.getcwd(), avg_emg_path))
        self.classified_data = None

    def update_pos_and_avg_graph(self, classif_region_pos):
        self.add_classif_class_number()
        try:
            classified_type = self.classified_data[int(classif_region_pos)]
            self.num.setHtml(str(classified_type))
            self.curve.setData(self.avg_emg_class_type[classified_type])
        except IndexError as e:
            print(e)
            
    def update_classif_region_plot(self, data):
        self.classif_region_curve.setData(data)

    def add_classif_class_number(self):
        html = f'{self.classif_type}'
        self.num.setHtml(html)
        self.num.setPos(0, 0.5)
        self.plot.addItem(self.num)
