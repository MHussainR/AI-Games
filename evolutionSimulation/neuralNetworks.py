import numpy as np

# Neural Network for controlling the player
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialize the neural network with input, hidden, and output layer sizes
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        # Initialize weights and biases with random values
        self.weights_ih = np.random.randn(self.hidden_size, self.input_size)
        self.weights_ho = np.random.randn(self.output_size, self.hidden_size)
        self.bias_h = np.random.randn(self.hidden_size, 1)
        self.bias_o = np.random.randn(self.output_size, 1)

    def forward(self, inputs):
        # Perform forward propagation through the neural network
        inputs = np.array(inputs).reshape(-1, 1)
        hidden = np.dot(self.weights_ih, inputs) + self.bias_h
        hidden = np.tanh(hidden)
        output = np.dot(self.weights_ho, hidden) + self.bias_o
        output = np.tanh(output)
        return output

    def get_action(self, state):
        # Get action (left or right) based on current state
        output = self.forward(state)
        return np.argmax(output)  # return 0 (left) or 1 (right)