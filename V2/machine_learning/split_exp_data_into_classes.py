# --General Packages--
# ProcessData
from generate_signal.file_reader import read_data_from_file
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.externals import joblib
# --My Packages--
from data_processing_pipeline.uniformize_data import uniformize_data

# Experiment protocol
# red midle forearm where watch and yellow one finger below still at the center
# of the forearm the red is connected at the bottom and the yellow on top at the
# pin N1P


class ProcessData:
    def __init__(self, exp_csv_dir, train_exp_folders, colors, SPLIT):
        """ """
        self.exp_csv_dir = exp_csv_dir
        self.train_exp_folders = train_exp_folders
        self.colors = colors
        self.SPLIT = SPLIT

        self.N_CLASS = len(train_exp_folders)

        self.X = [[] for _ in range(self.N_CLASS)]
        self.y = []

        self.l_data, self.l_t, self.l_exp = self.create_list_from_exp_data()

        self.save_emg_signal_if_event_stamp()

    def create_list_from_exp_data(self):
        """
        Creates features for an interval and normalizes them according to
        the maximum among all intervals.
        """
        l_data = []
        l_t = []
        l_exp = []

        for exp_no, folder_name in enumerate(self.train_exp_folders):
            folder_path = os.path.join(self.exp_csv_dir, folder_name)
            l_data.append([])
            l_t.append([])
            l_exp.append([])
            # Each folder contain many files contain a single type of exp (class)
            for file_name in os.listdir(folder_path)[self.SPLIT[0]:self.SPLIT[1]]:
                data, t, exp = read_data_from_file(
                        os.path.join(folder_path, file_name), N_CH=8)
                l_data[exp_no].append(np.array(data))
                l_t[exp_no].append(np.array(t))
                l_exp[exp_no].append(np.array(exp))

        return l_data, l_t, l_exp

    def save_emg_signal_if_event_stamp(self):
        # Look at all data with their corresponding experiment
        for class_num, class_data in enumerate(self.l_data):                   # TODO: ALEXM: Try to decrease the number of for loops if possible
            # Go over all the experiment in the folder
            for exp_no, exp in enumerate(class_data):
                events_pos = np.ravel(
                        np.where(self.l_exp[class_num][exp_no]))
                for pos in events_pos:
                    # Keep only the 1st electrodes that were used in this exp
                    for ch_data in exp[:1]:
                        self.save_emg_in_proper_class_list(
                                ch_data[pos-20:pos+160], class_num, exp_no)
            plt.show()

    def save_emg_in_proper_class_list(#OK
                self, one_ch_data, class_num, exp_no, plot_data=False):
        one_ch_data = uniformize_data(one_ch_data, len(one_ch_data))
        # Split in train and test set
        self.X[class_num].append(
                one_ch_data.reshape((len(one_ch_data), 1)))                                   # TODO: ALEXM: change the indice from the number of the folder it is reading fro
        self.y.append(class_num)
        # plot
        if plot_data and class_num == 0:
            plt.plot(one_ch_data)
            plt.title(f'class_num: {class_num}')
            plt.show()


def find_emg_avg_for_every_ch(class_type, colors, N_CLASS_TYPE): #OK
    avg_emg_class_type = [[] for _ in range(N_CLASS_TYPE)]
    # Plot all signal collected of one type in the same graph
    for ch, emg_ch in enumerate(class_type):
        avg_emg_class_type[ch] = np.mean(emg_ch, axis=0)
        for emg_signal in emg_ch:
            plt.plot(emg_signal, color=colors[ch], alpha=0.2)
    plt.title('YO')
    plt.show()

    # plt show average type
    for ch in range(len(class_type)):
        plt.plot(avg_emg_class_type[ch])
        plt.title('allow')
    plt.show()

    return avg_emg_class_type


'''
def show_signal_sum_with_error(linear_class_type_train, colors):
    df = pd.DataFrame()
    linear_class_type_train = [np.array(l) for l in linear_class_type_train]
    for i, signal_type in enumerate(linear_class_type_train):
        df = pd.DataFrame(signal_type.T)
        ax = sns.tsplot(data=df.T.values)
        mean = df.mean(axis=1)
        std = df.std(axis=1)
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

def train_classifier(x_train, y_train):
    clf = svm.LinearSVC()
    clf.fit(x_train, y_train)
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
            print('Predicted type', predicted)
            print('Real type', one_type)

    print('accuracy: ', (len(y_test)-error) / len(y_test))

'''

def create_ys(Xs):
    y_train = []
    for i in range(len(Xs)):
        for _ in range(len(Xs[i])):
            y_train.append(i)
    return np.array(y_train)

def create_proper_dim(X):
    X_2D = []                                                                  # Use np. functionnality instead
    for X_class in X:
        for event in X_class:
            X_2D.append(event)
    return np.array(X_2D)


def main():
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
    curr_base_path = os.getcwd()
    os.chdir('..')
    project_base_path = os.getcwd()
    exp_dir = os.path.join(project_base_path, 'learning_experiments_csv')
    exp_files_list = os.listdir(exp_dir)

    # Train data:
    process_data = ProcessData(exp_dir, exp_files_list, colors, (0, 4))
    x_train = process_data.X
    y_train = process_data.y
    print('HERE')
    # Test data:
    process_data = ProcessData(exp_dir, exp_files_list, colors, (4, 6))
    x_test = process_data.X
    y_test = process_data.y
    # Validation data:
    process_data = ProcessData(exp_dir, exp_files_list, colors, (7, 8))
    x_val = process_data.X
    y_val = process_data.y

    # Find average
    # avg_emg_class_type = find_emg_avg_for_every_ch(
    #         x_train, colors, len(exp_files_list))
    # print('Saving the average signal types...')
    #
    os.chdir(curr_base_path)
    # np.save('avg_emg_class_type', avg_emg_class_type)


    # show_signal_sum_with_error(linear_class_type_train, colors)

    # X, y = train_test_split(class_type_train)
    # X_test, y_test = train_test_split(class_type_test)

    # x_train = create_proper_dim(x_train)
    # x_test = create_proper_dim(x_test)

    # clf = train_classifier(x_train, y_train)
    # find_classifier_accuracy(x_test, y_test, clf)

    # Save
    np.save('./np_data/x_train', x_train)
    np.save('./np_data/y_train', y_train)
    np.save('./np_data/x_test', x_test)
    np.save('./np_data/y_test', y_test)
    np.save('./np_data/x_val', x_val)
    np.save('./np_data/y_val', y_val)


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
