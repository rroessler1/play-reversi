class Layer:
    def __init__(self):
        self.params = []
        self.previous = None
        self.next = None
        self.input_data = None
        self.output_data = None
        self.input_delta = None
        self.output_delta = None

    def add_after_layer(self, layer):
        self.previous = layer
        layer.next = self

    def forward(self):
        raise NotImplementedError

    def backward(self):
        raise NotImplementedError

    def get_forward_input(self):
        if self.previous is not None:
            return self.previous.output_data
        else:
            return self.input_data

    def get_backward_input(self):
        if self.next is not None:
            return self.next.output_delta
        else:
            return self.input_delta

    def clear_deltas(self):
        pass

    def update_params(self, learning_rate):
        pass

    def describe(self):
        raise NotImplementedError
