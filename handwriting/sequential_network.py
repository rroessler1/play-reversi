import random
from handwriting import mse
from typing import List
from handwriting.layer import Layer
import numpy as np


class SequentialNetwork:
    def __init__(self, loss=None):
        self.layers: List[Layer] = []
        self.loss = loss if loss else mse.MSE()

    def add(self, layer: Layer):
        self.layers.append(layer)
        if len(self.layers) > 1:
            self.layers[-1].add_after_layer(self.layers[-2])

    def train(self, training_data, num_epochs: int, mini_batch_size: int, learning_rate: float, test_data = None):
        for epoch_number in range(num_epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k : k + mini_batch_size] for k in range(0, len(training_data) - mini_batch_size, mini_batch_size)]
            for mini_batch in mini_batches:
                print("Training mini batch")
                self.train_batch(mini_batch, learning_rate)
            print(f"Epoch {epoch_number}: Training data: {self.evaluate(training_data)} / {len(training_data)}")
            if test_data:
                print(f"Epoch {epoch_number}: {self.evaluate(test_data)} / {len(test_data)}")
            else:
                print(f"Epoch {epoch_number} complete")

    def train_batch(self, batch, learning_rate):
        self.forward_backward(batch)
        self.update(batch, learning_rate)

    def update(self, batch, learning_rate):
        # TODO: this seems wrong, shouldn't it be learning_rate / (len(data) / len(batch))?
        learning_rate = learning_rate / len(batch)
        for layer in self.layers:
            layer.update_params(learning_rate)
        for layer in self.layers:
            layer.clear_deltas()

    def forward_backward(self, batch):
        for x, y in batch:
            self.layers[0].input_data = x
            for layer in self.layers:
                layer.forward()
            self.layers[-1].input_delta = self.loss.loss_derivative(self.layers[-1].output_data, y)
            for layer in reversed(self.layers):
                layer.backward()

    def single_forward(self, x):
        self.layers[0].input_data = x
        for layer in self.layers:
            layer.forward()
        return self.layers[-1].output_data

    def evaluate(self, test_data):
        test_results = [(
            np.argmax(self.single_forward(x)),
            np.argmax(y)
        ) for x, y in test_data]
        return sum(int(x == y) for x, y in test_results)