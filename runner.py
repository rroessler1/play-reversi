from handwriting import load
from handwriting import sequential_network
from handwriting.activation_layer import ActivationLayer
from handwriting.dense_layer import DenseLayer

training_data, test_data = load.load_data()
network = sequential_network.SequentialNetwork()
network.add(DenseLayer(784, 392))
network.add(ActivationLayer(392))
network.add(DenseLayer(392, 196))
network.add(ActivationLayer(196))
network.add(DenseLayer(196, 10))
network.add(ActivationLayer(10))

network.train(training_data[:11], num_epochs=10, mini_batch_size=10, learning_rate=3.0, test_data=test_data[:100])

