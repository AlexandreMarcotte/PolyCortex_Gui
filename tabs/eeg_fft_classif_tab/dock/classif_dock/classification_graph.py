from sklearn.externals import joblib
import os
import numpy as np
import pyqtgraph as pg
from collections import deque
from time import time

from data_processing_pipeline.uniformize_data import uniformize_data

class ClassifGraph:
    def __init__(self, gv, show_classif_plot, n_classif_plot):
        self.gv = gv
        clf_path = 'machine_learning/linear_svm_fitted_model.pkl'
        self.clf = joblib.load(os.path.join(os.getcwd(), clf_path))
        self.last_classif = np.array([0 for _ in range(15)])
        self.i = 0
        # Classification
        self.show_classif_plot = show_classif_plot
        self.init_show_classif()
        # n classification plot
        N_DATA = 200
        self.N_CLASSIF_TYPE = 3
        self.pen_color = ['r', 'b', 'g']
        self.n_classif_plot = n_classif_plot
        self.n_classif_queue = [deque(np.zeros(N_DATA), maxlen=N_DATA) \
                                for _ in range(self.N_CLASSIF_TYPE)]
        self.curve_n_classif = []
        self.REFRACT_PERIOD_T = 0.7
        self.refract_period_init_t = 0
        self.is_refract_period = False
        for ch in range(self.N_CLASSIF_TYPE):
            self.curve_n_classif.append(
                n_classif_plot.plot(deque(np.zeros(N_DATA), maxlen=N_DATA)))

    def init_show_classif(self):
        self.x = np.arange(9)
        self.y = np.array(np.zeros(9))
        self.bg = pg.BarGraphItem(x=self.x, height=self.y, width=1, brush='b')
        self.show_classif_plot.addItem(self.bg)

    def update_all(self):
        self.classify_incoming_data()
        self.update_bar_chart_plotting()
        self.update_n_classif_plotting()

    def classify_incoming_data(self):
        data_queue = np.array(self.gv.data_queue[3])
        emg_signal = data_queue[-170:]
        # Evaluate the classificaiton type
        if emg_signal.any():  # if all not all zero array
            # Uniformize data to help for prediction
            emg_signal = uniformize_data(emg_signal, len(emg_signal))
            # Prediction
            class_type = self.clf.predict([emg_signal])[0]
        else:
            class_type = 0
        self.last_classif[self.i] = class_type

        # update refracting period to false if the refraction time is passed
        if self.is_refract_period:
            if time() - self.refract_period_init_t > self.REFRACT_PERIOD_T:
                self.is_refract_period = False
        else:
            self.y = np.bincount(self.last_classif, minlength=9)
        # Keep track of the classification type at each itt to live graph it
        for i, classif_type in enumerate([0, 6, 7]):
            self.n_classif_queue[i].append(self.y[classif_type])
        # Select the event of a certain type if over a threshold of firering
        # Type CLOSE
        if self.y[6] >= 4:
            self.y = np.array(np.zeros(9))
            self.gv.last_classified_type[0] = 6
            self.refract_period_init_t = time()
            self.is_refract_period = True
        # Type PINCH
        elif self.y[7] >= 4:
            self.y = np.array(np.zeros(9))
            self.gv.last_classified_type[0] = 7
            self.refract_period_init_t = time()
            self.is_refract_period = True

        # Increase itt
        self.i += 1
        if self.i == 10:
            self.i = 0

    def update_bar_chart_plotting(self):
        # Remove All item from the graph
        self.show_classif_plot.clear()
        self.bg = pg.BarGraphItem(x=self.x, height=self.y, width=1, brush='b')
        self.show_classif_plot.addItem(self.bg)

    def update_n_classif_plotting(self):
        for classif_type in range(self.N_CLASSIF_TYPE):
            # Don't show the 0 values it's redondant                           # TODO: ALEXM Remove it in the dataqueue
            if classif_type:
                self.curve_n_classif[classif_type].setData(
                    self.n_classif_queue[classif_type])
                self.curve_n_classif[classif_type].setPen(
                                                self.pen_color[classif_type])




