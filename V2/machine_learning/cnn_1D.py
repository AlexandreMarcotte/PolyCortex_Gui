# --General Packages--
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.pooling import MaxPooling1D
from keras.optimizers import SGD, Adagrad, Adadelta, Adam, Adamax, Nadam
from keras.utils.np_utils import to_categorical
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import os


class Learner:
    def __init__(self, path_till_load_file='machine_learning/np_data'):
        self.path_till_load_file = path_till_load_file

        self.n_classes = 3
        self.load_all_data()
        self.init_cnn_variables()

    def load_all_data(self):
        self.x_train, self.y_train = self.load_data(
                'x_train.npy', 'y_train.npy')
        self.x_test, self.y_test = self.load_data(
                'x_test.npy', 'y_test.npy')
        self.x_val, self.y_val = self.load_data('x_val.npy', 'y_val.npy')
        self.y_val = to_categorical(self.y_val, num_classes=3)

    def load_data(self, x_f_name, y_f_name):

        path = os.path.join(os.getcwd(), self.path_till_load_file)
        x = np.load(os.path.join(path, x_f_name))
        x = x.reshape(-1, *x.shape[-2:])
        y= np.load(os.path.join(path, y_f_name))

        return x, y

    def init_cnn_variables(self):
        self.n_epoch = 200
        self.batch_size = 60
        self.n_filters = [90, 20]
        self.n_pool = 10
        self.n_conv = [12, 10]
        self.dropout = [0.5, 0.5]
        self.add_second_layout = False
        self.selected_optimizer = 'Adam'
        self.optimizer, self.optimizer_params = self.select_optimizer()
        self.activation_unit = 'relu'

        self.model_name = 'poly3_model.h5'
        self.save_model_path = os.path.join('machine_learning/models/', self.model_name)
        self.load_model_path = os.path.join('machine_learning/models/', self.model_name)

    def train_cnn(self):
        """
        """
        y_train = to_categorical(self.y_train, num_classes=self.n_classes)
        y_test = to_categorical(self.y_test, num_classes=self.n_classes)

        shape_ord = (self.x_train.shape[1], 1)

        optimizer, _ = self.select_optimizer()

        model = Sequential()
        model.add(Conv1D(
                self.n_filters[0], (self.n_conv[0]), padding='valid',
                input_shape=shape_ord))
        model.add(Activation(self.activation_unit))

        model.add(MaxPooling1D(pool_size=(self.n_pool)))
        model.add(Dropout(self.dropout[0]))

        # If we want to use a 2 level CNN
        if self.add_second_layout:
            model.add(
                    Conv1D(self.n_filters[1], (self.n_conv[1]),
                           padding='valid'))
            model.add(Activation(self.activation_unit))
            model.add(Dropout(self.dropout[1]))

        model.add(Flatten())
        model.add(Dense(self.n_classes))
        model.add(Activation('softmax'))
        model.compile(
                loss='categorical_crossentropy', optimizer=optimizer,
                metrics=['accuracy'])

        # Training the model
        hist = model.fit(
                self.x_train, y_train, batch_size=self.batch_size,
                epochs=self.n_epoch, verbose=2,
                validation_data=(self.x_test, y_test))

        return hist, model

    def select_optimizer(self):
        if self.selected_optimizer == 'SGD':
            optimizer = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        elif self.selected_optimizer == 'Adagrad':
            optimizer = Adagrad(lr=0.01, epsilon=1e-08, decay=0.0)
        elif self.selected_optimizer == 'Adadelta':
            optimizer = Adadelta(lr=1.0, rho=0.95, epsilon=1e-08, decay=0.0)
        elif self.selected_optimizer == 'Adam':
            optimizer = Adam(
                    lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08,
                    decay=0.0)
            optimizer_params = {
                    'lr': 0.01, 'beta_1':0.9, 'beta_2':0.999,
                    'epsilon': 1e-08, 'decay': 0.0}
        elif self.selected_optimizer == 'Nadam':
            optimizer = Nadam(
                    lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None,
                    schedule_decay=0.004)
        elif self.selected_optimizer == 'Nadam':
            optimizer = Adamax(
                    lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None,
                    decay=0.0)
        return optimizer, optimizer_params

    def model_loss_and_accuracy(self):
        return model.evaluate(learner.x_val, learner.y_val, verbose=0)

    def plot_results(self, hist):
        plt.figure()
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.plot(hist.history['loss'])
        plt.plot(hist.history['val_loss'])
        plt.legend(['Training', 'Validation'])
        # plot of the accuracy
        plt.figure()
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.plot(hist.history['acc'])
        plt.plot(hist.history['val_acc'])
        plt.legend(['Training', 'Validation'], loc='lower right')
        plt.show()

    def show_evaluation_plots(self):
        predictions, predictions_proportion = self.predict()
        for pred, real, sig in zip(predictions, self.y_val, self.x_val):
            plt.plot(sig)
            plt.title(f'prediction {pred}, real {real}')
            plt.show()
            sleep(0.5)

    def load_model(self):
        return load_model(self.load_model_path)

    def predict(self):
        model = self.load_model()
        predictions = model.predict(self.x_val).argmax(-1)
        predictions_proportion = model.predict(self.x_val)
        return predictions, predictions_proportion


if __name__ == '__main__':
    learner = Learner()
    hist, model = learner.train_cnn()
    learner.plot_results(hist)

    model.save(learner.save_model_path)

    # learner.show_evaluation_plots()



