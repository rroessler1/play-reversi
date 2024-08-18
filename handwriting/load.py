import numpy as np
import os

dirname = os.path.dirname(__file__)


def encode_label(digit):
    v = np.zeros((10, 1))
    v[digit] = 1.0
    return v


def shape_data(data):
    features = [np.reshape(x, (784, 1)) for x in data[0]]
    labels = [encode_label(y) for y in data[1]]
    return list(zip(features, labels))


def load_data():
    f = np.load(os.path.join(dirname, "mnist.npz"))
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']
    f.close()
    return shape_data((x_train, y_train)), shape_data((x_test, y_test))
