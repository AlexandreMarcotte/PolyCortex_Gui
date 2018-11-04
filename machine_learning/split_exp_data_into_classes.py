# ProcessData
from generated_signal import read_data_from_file
import os
import numpy as np
import matplotlib.pyplot as plt
# Visualisation of all signal and the std deviation between the same type
import seaborn as sns
import pandas as pd
from pandas.plotting import andrews_curves
# Classification
import math
from sklearn import svm

import time
from sklearn.externals import joblib
# My packages
from signal_manipulation import uniformize_data


class ProcessData:
    def __init__(self, base_path, list_experiment_csv, colors):
        """
        Object attributes:
        ----------
        path : str
            String of the folder where the experiment .csv file are located
        l_data : list of np.array()
            [np.array(t1:[ch1, ch2, ..., ch8]), np.array(t2:[ch1, ch2, ..., ch8]), ...]
            List of all the signal collected from all 8 channels during one
            one experiment. Every np.array containted in the list is filled
            with the value of one experiment
        l_t : list
            List of all the timestamp corresponding to all sample in l_data
        l_exp : list
            List of classification type (classification type possible are:
            0: no event
            1: event first electrode on left arm (left one) *1
            2: event second electrode on left arm (right one)
            3: event first electrode on right arm (left one)
            4: event second electrode on right arm (right one)
            * Side when the wrist is facing you
            The number 1-4 are spawn in the experimentation at the moment you
            should start the corresponding action. Therefore the action is mostly
            contained after this point but can also be a bit before if you
            'jump the gun' when doing the action.
        """
        self.base_path = base_path
        self.list_experiment_csv = list_experiment_csv
        self.colors = colors
        # T = Type, E = Electrod
        # T1:Pinchleft T2:CloseHandleft  (T3 and T4 => left)
        # E1:Left electrode on left arm
        # E2:Right electrode on left arm
        # E3:Left electrode on right arm
        # E4:Right electrode on right arm
        # [[nosignal],[T1;E1],[T1E2],[T2;E1],[T2;E2],[T3;E3],[T3;E4],[T4;E3],[T4;E4]]
        self.class_type = [[] for _ in range(9)]
        self.l_data = []
        self.l_t = []
        self.l_exp = []

        self.generate_class_type_list()

    def generate_class_type_list(self):
        self.create_lst_from_experiment_data()
        self.save_emg_signal_if_event_stamp()
        return self.class_type

    def create_lst_from_experiment_data(self):
        """
        Creates features for an interval and normalizes them according to the
        maximum among all intervals.
        """
        for dir in self.list_experiment_csv:
            data, t, exp = read_data_from_file(os.path.join(self.base_path, dir), n_ch=8)
            self.l_data.append(np.array(data))
            self.l_t.append(np.array(t))
            self.l_exp.append(np.array(exp))

    def save_emg_signal_if_event_stamp(self):
        # Look at all data with their corresponding experiment
        for exp, data in zip(self.l_exp, self.l_data):
            for no, emg_type in enumerate(exp):
                # Keep only first electrodes that were used in this experiment
                for ch, one_ch_data in enumerate(data[:4]):
                    emg_type = int(emg_type)
                    if emg_type != 0:
                        self.save_emg_in_proper_class_list(one_ch_data, no,
                                                           ch, emg_type)

    def save_emg_in_proper_class_list(self, one_ch_data, no, ch, emg_type,
                                      plot_data=False):
        emg_signal = np.array(one_ch_data[no-60:no+110])
        no_emg_signal = np.array(one_ch_data[no+100:no+270])
        # Uniformize data
        emg_signal = uniformize_data(emg_signal, len(emg_signal))
        no_emg_signal = uniformize_data(no_emg_signal, len(no_emg_signal))
        # Classify the signal at the right position in the list
        if emg_type == 1 or emg_type == 2:
            if ch == 0 or ch == 1:
                pos = ch * 2 + emg_type  # => 1,2,3,4
                self.class_type[pos].append(emg_signal)
                if len(no_emg_signal) == 170:
                    self.class_type[0].append(no_emg_signal)
        if emg_type == 3 or emg_type == 4:
            if ch == 2 or ch == 3:
                pos = (ch-1)*2 + emg_type  # => 5,6,7,8
                self.class_type[pos].append(emg_signal)
                if len(no_emg_signal) == 170:
                    self.class_type[0].append(no_emg_signal)
                # Plot
                if plot_data:
                    plt.plot(emg_signal, color=colors[color_no])


def find_emg_avg_for_every_ch(class_type, colors):
    avg_emg_class_type = [[] for _ in range(9)]
    # Plot all signal collected of one type in the same graph
    for ch, emg_ch in enumerate(class_type):
        avg_emg_class_type[ch] = np.mean(emg_ch, axis=0)
        for emg_signal in emg_ch:
            plt.plot(emg_signal, color=colors[ch], alpha=0.2)
        plt.show()

    # plt show average type
    for ch in range(9):
        plt.plot(avg_emg_class_type[ch])
        plt.show()

    return avg_emg_class_type


def show_signal_sum_with_error(linear_class_type_train, colors):
    df = pd.DataFrame()
    linear_class_type_train = [np.array(l) for l in linear_class_type_train]
    for i, signal_type in enumerate(linear_class_type_train):
        df = pd.DataFrame(signal_type.T)
        ax = sns.tsplot(data=df.T.values)
        mean = df.mean(axis=1)
        std  = df.std(axis=1)
        ax.errorbar(df.index, mean, yerr=std, fmt='-', color=colors[i])

        plt.show()


def train_test_split(linear_class_type):
    n_data = len(linear_class_type[0])
    # split_pos = math.floor(n_data*0.70)
    X = []
    y = []
    for type_no, one_type_sig in enumerate(linear_class_type):
        for i, one_sig in enumerate(one_type_sig):
            # Keep only signal type 6 or 7 for binary classification
            if type_no == 0 or type_no == 6 or type_no == 7:
                X.append(np.array(one_sig))
                y.append(type_no)

    return X, y


def train_classifier(X, y):
    clf = svm.LinearSVC()
    print('len', len(X[0]))
    clf.fit(X, y)
    joblib.dump(clf, 'linear_svm_fitted_model.pkl')
    return clf


def find_classifier_accuracy(X_test, y_test, clf):
    print('-----------')
    error = 0
    for one_sig, one_type in zip(X_test, y_test):
        predicted = clf.predict([one_sig])
        # print('Predicted type', predicted)
        # print('Real type', one_type)
        if predicted[0] != one_type:
            error += 1
            # plt.plot(one_sig)
            # plt.show()
            # print('Predicted type', predicted)
            # print('Real type', one_type)

    print('accuracy: ', (len(y_test)-error) / len(y_test))


def main():
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
    base_path = '/home/alex/Documents/CODING/2018/openBCI_eeg_gui/experiment_csv'
    list_experiment_csv = os.listdir(base_path)
    # Train:
    train_exp = list_experiment_csv[:2]
    process_data = ProcessData(base_path, train_exp, colors)
    class_type_train = process_data.class_type
    avg_emg_class_type = find_emg_avg_for_every_ch(class_type_train, colors)
    print('Saving the average signal types...')
    np.save('avg_emg_class_type', avg_emg_class_type)

    # show_signal_sum_with_error(linear_class_type_train, colors)
    # Test:
    test_exp = list_experiment_csv[2:]
    process_data = ProcessData(base_path, test_exp, colors)
    class_type_test = process_data.class_type

    X, y = train_test_split(class_type_train)
    X_test, y_test = train_test_split(class_type_test)

    clf = train_classifier(X, y)

    find_classifier_accuracy(X_test, y_test, clf)


if __name__ == '__main__':
    main()

# TODO: ALEXM Split the data first 2 experimentation = training and last experimentation = Testing
# it will be closer to a real life situation
#
# Then try to do the live classification (by keeping the position of the predicted array as the
# first 170 value in the queue (and as the queue is moving forward it will change every time
# we do an other prediction
#
# Then do the tab to facilitate further prediction by implementing the two graph
# Graph where there are prediction value as a percentage of each class to have
# a good visualization of how the svm works
