from sklearn.externals import joblib
from keras.models import load_model
import os
import numpy as np
import pyqtgraph as pg
from collections import deque
from time import time
import matplotlib.pyplot as plt

from data_processing_pipeline.uniformize_data import uniformize_data

class ClassifGraph:
    def __init__(self, gv, show_classif_plot, n_classif_plot):
        self.N_CLASSIF_TYPE = 3
        self.gv = gv

        # Classifier
        clf_path = 'machine_learning/linear_svm_fitted_model.pkl'
        # self.clf = joblib.load(os.path.join(os.getcwd(), clf_path))
        self.model = load_model(
                '/home/alex/Desktop/openBCI_eeg_gui/machine_learning/cyn_model.h5')

        self.CLASSIF_MEMORY_LEN = 5
        self.last_classif = np.array(
                [0 for _ in range(self.CLASSIF_MEMORY_LEN)])
        self.i = 0
        # Classification
        self.show_classif_plot = show_classif_plot
        self.init_show_classif()
        # n classification plot
        N_DATA = 200
        self.pen_color = ['r', 'b', 'g']
        self.n_classif_plot = n_classif_plot
        self.n_classif_queue = [deque(np.zeros(N_DATA), maxlen=N_DATA)
                                for _ in range(self.N_CLASSIF_TYPE)]
        self.curve_n_classif = []
        self.REFRACT_PERIOD_T = 1
        self.refract_period_init_t = 0
        self.is_refract_period = False
        for ch in range(self.N_CLASSIF_TYPE):
            self.curve_n_classif.append(
                    n_classif_plot.plot(
                            deque(np.zeros(N_DATA), maxlen=N_DATA)))

    def init_show_classif(self):
        self.x = np.arange(self.N_CLASSIF_TYPE)
        self.y = np.array(np.zeros(self.N_CLASSIF_TYPE))
        self.bg = pg.BarGraphItem(x=self.x, height=self.y, width=1, brush='b')
        self.show_classif_plot.addItem(self.bg)

    def update_all(self):
        self.classify_incoming_data()
        self.update_bar_chart_plotting()
        self.update_n_classif_plotting()

    def classify_incoming_data(self):
        data_queue = np.array(self.gv.data_queue[0])
        emg_signal = data_queue[-180:]
        # Evaluate the classificaiton type
        if emg_signal.any():  # if all not all zero array
            # Uniformize data to help for prediction
            emg_signal = uniformize_data(emg_signal, len(emg_signal))
            # Prediction
            # class_type = self.clf.predict([emg_signal])[0]
            emg_signal = np.reshape(emg_signal, (1, 180, 1))
            class_type = self.model.predict(emg_signal).argmax(-1)
        else:
            class_type = 0
        self.last_classif[self.i] = class_type

        SHOW_PLOT = False
        if SHOW_PLOT:
            print('last_classif: ', self.last_classif)
            self.show_plt_of_current_classif(emg_signal, class_type)

        # update refracting period to false if the refraction time is passed
        if self.is_refract_period:
            if time() - self.refract_period_init_t > self.REFRACT_PERIOD_T:
                self.is_refract_period = False
        else:
            self.y = np.bincount(
                    self.last_classif, minlength=self.N_CLASSIF_TYPE)
        # Keep track of the classification type at each itt to live graph it
        for no_class in range(self.N_CLASSIF_TYPE):
            self.n_classif_queue[no_class].append(self.y[no_class])
        # Select the event of a certain type if over a threshold of firering
        # Type CLOSE
        if self.y[1] >= 1:
            self.update_after_classif(1)

        elif self.y[0] >= 2:
            self.update_after_classif(0)


        self.i += 1
        if self.i == self.CLASSIF_MEMORY_LEN:
            self.i = 0

    def show_plt_of_current_classif(self, emg_signal, class_type):
        plt.plot(emg_signal[0])
        plt.title(f'classif_type: {class_type}')
        plt.show()

    def update_after_classif(self, classif_type ):
        self.y = np.array(np.zeros(self.N_CLASSIF_TYPE))
        self.gv.last_classified_type = classif_type
        self.refract_period_init_t = time()
        self.is_refract_period = True
    # Type PINCH

    def update_bar_chart_plotting(self):
        # Remove All item from the graph
        self.show_classif_plot.clear()
        self.bg = pg.BarGraphItem(x=self.x, height=self.y, width=1, brush='b')
        self.show_classif_plot.addItem(self.bg)

    def update_n_classif_plotting(self):
        for classif_type in range(self.N_CLASSIF_TYPE):
            # Don't show the 2 values because its not action                           # TODO: ALEXM Remove it in the dataqueue
            if classif_type in [0, 1]:
                self.curve_n_classif[classif_type].setData(
                        self.n_classif_queue[classif_type])
                self.curve_n_classif[classif_type].setPen(
                        self.pen_color[classif_type])
