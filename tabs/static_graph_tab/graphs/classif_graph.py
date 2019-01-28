# -- General Packages --
from sklearn.externals import joblib
import os
import numpy as np
# -- My Packages --
from data_processing_pipeline.uniformize_data import uniformize_data
from ... static_graph_tab.graphs.graph import Graph

class ClassifGraph(Graph):
    def __init__(self, gv):
        super().__init__()
        self.gv = gv

        clf_path = 'machine_learning/linear_svm_fitted_model.pkl'
        self.clf = joblib.load(os.path.join(os.getcwd(), clf_path))
        self.classif_interval = 250

    def classify_data(self, data):
        classified_data = []
        data = np.array(data)
        pos = 0
        # While we haven't reach the end of the data
        while pos + self.gv.emg_signal_len < len(data):
            d = data[0 + pos:self.gv.emg_signal_len + pos]
            # If the array is not filled with only 0 values
            if d.any():
                d = uniformize_data(d, len(d))
                # classif_value = self.clf.predict([d])[0]
            else:
                classif_value = 0
            # set all the same type for all the interval of classification
            for _ in range(self.classif_interval):
                classified_data.append(classif_value)
            # Update pos for next classification of the type of the signal
            pos += self.classif_interval
        return classified_data