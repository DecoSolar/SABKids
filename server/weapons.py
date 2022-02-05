from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils
import os
import cv2
from keras.preprocessing.image import img_to_array
import numpy as np
import tensorflow as tf
from PIL import Image

x = []
m, n = 50, 50


def detect_weapons(path: str):
    model = tf.keras.models.load_model("weapons_models/model_latest.h5")
    x = []
    im = Image.open(path)
    imrs = im.resize((m, n))
    imrs = img_to_array(imrs) / 255
    imrs = imrs.transpose(2, 0, 1)
    imrs = imrs.reshape(3, m, n)
    x.append(imrs)
    x = np.array(x)
    result2 = str(model.predict(x)[0]).replace('[', '').replace(']', '').split(' ')
    m_list = ["knife", "gun", "rifle"]
    res = [{a: contains(b)} for (a, b) in zip(m_list, result2)]
    return res


def contains(val):
    clear = str(val).split('.')[0]
    if not clear:
        return False
    return int(clear) > int(5)
