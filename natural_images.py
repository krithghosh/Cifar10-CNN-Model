# -*- coding: utf-8 -*-
"""Natural_Images.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m0vNABcqkqBZ9V3kIP_bjj5dDcZbER0x
"""

import numpy as np
from keras.utils import np_utils
import matplotlib.pyplot as plt
import os
from keras.datasets import cifar10
from keras.preprocessing.image import img_to_array, load_img

img_size=32
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
print('Loading done !')

no_of_classes = len(np.unique(y_train))
print(no_of_classes)

# Converts an integer to binary matrix as we would use categorical_crossentropy
y_train = np_utils.to_categorical(y_train, no_of_classes)
y_test = np_utils.to_categorical(y_test, no_of_classes)

x_test, x_valid = x_test[5000:], x_test[:5000]
y_test, y_valid = y_test[5000:], y_test[:5000]
print('Validation X : ', x_valid.shape)
print('Validation y : ', y_valid.shape)
print('Test X : ', x_test.shape)
print('Test y : ', y_test.shape)

x_train = x_train.astype('float32')/255
x_valid = x_valid.astype('float32')/255
x_test = x_test.astype('float32')/255

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.layers import Activation, Dense, Flatten, Dropout
from keras.callbacks import ModelCheckpoint

model = Sequential()
model.add(Conv2D(filters = 32, kernel_size = 2, input_shape=(img_size,img_size,3), padding='same'))
model.add(Activation('relu'))
model.add(BatchNormalization())

model.add(Conv2D(filters = 32, kernel_size = 2, padding='same'))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters = 64,kernel_size = 2, padding='same'))
model.add(Activation('relu'))
model.add(BatchNormalization())

model.add(Conv2D(filters = 64, kernel_size = 2, padding='same'))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters = 128,kernel_size = 2, padding='same'))
model.add(Activation('relu'))
model.add(BatchNormalization())

model.add(Conv2D(filters = 128,kernel_size = 2, padding='same'))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=2))

model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(150))
model.add(Activation('relu'))
model.add(Dropout(0.4))
model.add(Dense(no_of_classes,activation = 'softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
checkpointer = ModelCheckpoint(filepath = 'weights_cifar10.hdf5', verbose = 1, save_best_only = True)

history = model.fit(x_train,y_train,
        batch_size = 32,
        epochs=10,
        validation_data=(x_valid, y_valid),
        callbacks = [checkpointer],
        verbose=2, shuffle=True)

def save_model(model):
    model_json = model.to_json()
    with open('model_cifar10.json', 'w') as json_file:
        json_file.write(model_json)

save_model(model)

from keras.models import model_from_json
json_file = open('model_cifar10.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

model.load_weights('weights_cifar10.hdf5')

score = model.evaluate(x_test, y_test, verbose=0)
print('Accuracy: ', score[1])

# Prediction
x_pred = []
files = os.listdir(pred_dir)
for file in files:
    x_pred.append(os.path.join(pred_dir, file))

def convert_image_to_array(files):
    images_as_array = []
    for file in files:
        images_as_array.append(img_to_array(load_img(file)))
    return images_as_array

x_pred = np.array(convert_image_to_array(x_pred))
x_pred = x_pred.astype('float32')/255

y_pred = model.predict(x_test)

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

target_labels = unpickle(labels_dir)

target_labels = [
    'airplane', 
    'automobile',
    'bird',
    'cat',
    'deer',
    'dog',
    'frog',
    'horse',
    'ship',
    'truck'
]

fig = plt.figure(figsize=(16, 9))
for i, idx in enumerate(np.random.choice(x_test.shape[0], size=16, replace=False)):
    ax = fig.add_subplot(4, 4, i + 1, xticks=[], yticks=[])
    ax.imshow(np.squeeze(x_test[idx]))
    pred_idx = np.argmax(y_pred[idx])
    actual_idx = np.argmax(y_test[idx])
    ax.set_title("{}".format(target_labels[pred_idx]), color=("green" if pred_idx == actual_idx else "red"))