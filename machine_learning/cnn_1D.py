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


def train_cnn(nb_classes, x_train, y_train, x_test, y_test):
    """
    """
    y_train = to_categorical(y_train, num_classes=nb_classes)
    y_test = to_categorical(y_test, num_classes=nb_classes)


    shape_ord = (x_train.shape[1], 1)
    nb_epoch = 500
    batch_size = 60
    # First layer
    nb_filters_1 = 90
    nb_pool = 10
    nb_conv1 = 12
    # Second layer
    add_second_layout = False
    nb_conv2 = 30
    nb_filters_2 = 2

    # OPTIMIZERS
    # optimizer = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    # optimizer = Adagrad(lr=0.01, epsilon=1e-08, decay=0.0)
    # optimizer = Adadelta(lr=1.0, rho=0.95, epsilon=1e-08, decay=0.0)
    optimizer = Adam(
            lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    # optimizer = Nadam(
    #         lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None,
    #         schedule_decay=0.004)
    # optimizer = Adamax(
    #         lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)

    model = Sequential()
    model.add(Conv1D(
            nb_filters_1, (nb_conv1), padding='valid', input_shape=shape_ord))
    model.add(Activation('relu'))

    model.add(MaxPooling1D(pool_size=(nb_pool)))
    model.add(Dropout(0.5))

    # If we want to use a 2 level CNN
    if add_second_layout:
        model.add(Conv1D(nb_filters_2, (nb_conv2), padding='valid'))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(
            loss='categorical_crossentropy', optimizer=optimizer,
            metrics=['accuracy'])

    # Training the model
    hist = model.fit(
            x_train, y_train, batch_size=batch_size, epochs=nb_epoch,
            verbose=2, validation_data=(x_test, y_test))

    return hist, model

def plot_results(hist):
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


if __name__ == '__main__':

    x_train = np.load('x_train.npy')
    x_train = x_train.reshape(-1, *x_train.shape[-2:])
    y_train = np.load('y_train.npy')

    x_test = np.load('x_test.npy')
    x_test = x_test.reshape(-1, *x_test.shape[-2:])
    y_test =np.load('y_test.npy')

    hist, model = train_cnn(
            nb_classes=3, x_train=x_train, y_train=y_train, x_test=x_test,
            y_test=y_test)
    plot_results(hist)

    # loss, accuracy = model.evaluate(x_val, y_val, verbose=0)
    # print('Test loss: ', loss)
    # print('Test accuracy: ', accuracy)

    x_val = np.load('x_val.npy')
    x_val = x_val.reshape(-1, *x_val.shape[-2:])
    print(x_val.shape)
    y_val = np.load('y_val.npy')
    y_val = to_categorical(y_val, num_classes=3)

    model.save('forearm_model.h5')
    model_loaded = load_model('forearm_model.h5')

    predictions = model_loaded.predict(x_val).argmax(-1)
    prediction_proportion = model_loaded.predict(x_val)
    # for pred, real, sig in zip(predictions, y_val, x_val):
    #     plt.plot(sig)
    #     plt.title(f'prediction {pred}, real {real}')
    #     plt.show()
    #     sleep(0.5)
