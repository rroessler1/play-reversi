from handwriting import utils
from handwriting.layer import Layer


class ActivationLayer(Layer):

    def __init__(self, input_dim):
        super(ActivationLayer, self).__init__()
        self.input_dim = input_dim
        self.output_dim = input_dim

    def forward(self):
        data = self.get_forward_input()
        self.output_data = utils.sigmoid(data)

    def backward(self):
        delta = self.get_backward_input()
        data = self.get_forward_input()
        self.output_delta = utils.sigmoid_prime(data) * delta

    def describe(self):
        print("|--" + self.__class__.__name__)
        print(" |-dimensions: ({},{})".format(self.input_dim, self.output_dim))