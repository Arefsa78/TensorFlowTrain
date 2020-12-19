from keras import layers, models, activations, losses, metrics, optimizers
import matplotlib.pyplot as plt
from numpy import array, random
import numpy as np
from make_data import make_all

# xin = open('xout', 'r')
# yin = open('yout', 'r')
#
# x = xin.readlines()
# y = yin.readlines()
#
# X = []
# Y = []
# for xx in x:
#     xxx = xx.split(' ')
#     X.append([float(xxx[0]), float(xxx[1])])
#
# for xx in y:
#     Y.append(float(xx))
#

X, Y = make_all()
X = array(X)
Y = array(Y)

data_size = X.shape[0]
train_size = int(data_size * 0.8)

randomize = np.arange(len(X))
np.random.shuffle(randomize)
X = X[randomize]
Y = Y[randomize]
print(X.shape, train_size)
train_datas = X[:train_size]
train_labels = Y[:train_size]
test_datas = X[train_size + 1:]
test_labels = Y[train_size + 1:]

network = models.Sequential()
network.add(layers.Dense(64, activation=activations.relu, input_shape=(12,)))
network.add(layers.Dense(16, activation=activations.relu))
network.add(layers.Dense(2, activation=activations.linear))
network.compile(optimizer=optimizers.Adam(), loss=losses.mse, metrics=[metrics.mse],)
history = network.fit(train_datas, train_labels,
                      epochs=100, batch_size=64,
                      validation_data=(test_datas, test_labels),
                      use_multiprocessing=True
                      )
# test_loss, test_acc = network.evaluate(test_datas, test_labels)
history_dict = history.history

loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
acc_values = history_dict['mean_squared_error']
val_acc_values = history_dict['val_mean_squared_error']

epochs = range(len(loss_values))
plt.figure(1)
plt.subplot(211)
plt.plot(epochs, loss_values, 'r--', label='Training loss')
plt.plot(epochs, val_loss_values, 'b--', label='Validation loss')
plt.title("train/test loss")
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.subplot(212)
plt.plot(epochs, acc_values, 'r--', label='Training mean_squared_error')
plt.plot(epochs, val_acc_values, '--', label='Validation mean_squared_error')
plt.title("train/test acc")
plt.xlabel('Epochs')
plt.ylabel('Acc')
plt.legend()
plt.show()
network.save('model.h5')


