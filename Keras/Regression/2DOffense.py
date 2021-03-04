from keras import layers, models, activations, losses, metrics, optimizers
import matplotlib.pyplot as plt
from numpy import array, random
import numpy as np
import pandas as pd
import os
import keras


def read_data(path_x, path_y):
    df_in = pd.read_csv(path_x)
    df_out = pd.read_csv(path_y)
    x = df_in.to_numpy()
    y = df_out.to_numpy()
    return x, y


path_x = './data/x.csv'
path_y = './data/y.csv'
x, y = read_data(path_x, path_y)
size = x.shape[0]
train_size = int(size * 0.9)

randomize = np.arange(len(x))
np.random.shuffle(randomize)
x = x[randomize]
y = y[randomize]
y = keras.utils.to_categorical(y, num_classes=4)

x_train = x[:train_size]
y_train = y[:train_size]
x_test = x[train_size + 1:]
y_test = y[train_size + 1:]
del x
del y
models_conf = [
    #[256], #92 92
    #[1024], #96 96
    #[8, 8], #82 82
    [32, 16], #88 88
    [32, 128],# 92 92
    [128, 32],
    [64, 32],
    [32, 16, 8],
    [64, 32, 16],
    [128, 64, 32],
    [128, 32, 8],
    [64, 4, 64],
    [32, 8, 32],
    [128, 64, 32, 16, 8],
    [256, 128, 64, 32, 16],
    [8], #82 82
    [64], #88 89
]

results = {}

def make_model(conf):
    network = models.Sequential()
    network.add(layers.Dense(32, activation=activations.relu, input_shape=(14,)))
    for n in conf:
        network.add(layers.Dense(n, activation=activations.relu))
    network.add(layers.Dense(4, activation=activations.softmax))
    network.compile(optimizer=optimizers.Adam(), loss=losses.categorical_crossentropy, metrics=['accuracy'])
    return network


for conf in models_conf:
    network = make_model(conf)
    history = network.fit(x_train, y_train,
                          epochs=20, batch_size=1024,
                          validation_data=(x_test, y_test),
                          use_multiprocessing=True
                          )
    history_dict = history.history

    loss_values = history_dict['loss']
    val_loss_values = history_dict['val_loss']
    acc_values = history_dict['accuracy']
    val_acc_values = history_dict['val_accuracy']

    epochs = range(len(loss_values))
    #plt.figure(1)
    #plt.subplot(211)

    #plt.plot(epochs, loss_values, 'r--', label='Training loss')
    #plt.plot(epochs, val_loss_values, 'b--', label='Validation loss')
    #plt.title("train/test loss")
    #plt.xlabel('Epochs')
    #plt.ylabel('Loss')
    #plt.legend()
    #plt.subplot(212)
    #plt.plot(epochs, acc_values, 'r--', label='Training mean_squared_error')
    #plt.plot(epochs, val_acc_values, '--', label='Validation mean_squared_error')
    #plt.title("train/test acc")
    #plt.xlabel('Epochs')
    #plt.ylabel('Acc')
    #plt.legend()
    #plt.title(str(conf))
#    plt.show()
    print(conf, max(history_dict['accuracy']), max(history_dict['val_accuracy']))
    results[str(conf)] = [max(history_dict['accuracy']), max(history_dict['val_accuracy'])]

print(results)

