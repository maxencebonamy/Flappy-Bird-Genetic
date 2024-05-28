import numpy as np


class NeuralNetwork:
	
	INPUT_SIZE = 3
	HIDDEN_SIZE = 5
	OUTPUT_SIZE = 1
	ACTIVATION_FUNCTION = np.tanh
	THRESHOLD = 1
	MUTATION_RATE = 0.5

	def __init__(self):
		self.__weights_input_hidden = np.random.randn(NeuralNetwork.INPUT_SIZE, NeuralNetwork.HIDDEN_SIZE)
		self.__weights_hidden_output = np.random.randn(NeuralNetwork.HIDDEN_SIZE, NeuralNetwork.OUTPUT_SIZE)
		self.__bias_hidden = np.random.randn(NeuralNetwork.HIDDEN_SIZE)
		self.__bias_output = np.random.randn(NeuralNetwork.OUTPUT_SIZE)

	@staticmethod
	def from_parents(parent1, parent2):
		child = NeuralNetwork()
		child.__weights_input_hidden = (parent1.__weights_input_hidden + parent2.__weights_input_hidden) / 2
		child.__weights_hidden_output = (parent1.__weights_hidden_output + parent2.__weights_hidden_output) / 2
		child.__bias_hidden = (parent1.__bias_hidden + parent2.__bias_hidden) / 2
		child.__bias_output = (parent1.__bias_output + parent2.__bias_output) / 2
		return child
	
	def copy(self):
		child = NeuralNetwork()
		child.__weights_input_hidden = np.copy(self.__weights_input_hidden)
		child.__weights_hidden_output = np.copy(self.__weights_hidden_output)
		child.__bias_hidden = np.copy(self.__bias_hidden)
		child.__bias_output = np.copy(self.__bias_output)
		return child

	def mutate(self):
		if np.random.rand() < NeuralNetwork.MUTATION_RATE:
			self.__weights_input_hidden += np.random.randn(*self.__weights_input_hidden.shape) * 0.1
			self.__weights_hidden_output += np.random.randn(*self.__weights_hidden_output.shape) * 0.1
			self.__bias_hidden += np.random.randn(*self.__bias_hidden.shape) * 0.1
			self.__bias_output += np.random.randn(*self.__bias_output.shape) * 0.1

	def predict(self, inputs):
		output = self.__forward(inputs)
		return output > NeuralNetwork.THRESHOLD

	def __forward(self, inputs):
		hidden = np.dot(inputs, self.__weights_input_hidden) + self.__bias_hidden
		hidden = NeuralNetwork.ACTIVATION_FUNCTION(hidden)
		output = np.dot(hidden, self.__weights_hidden_output) + self.__bias_output
		return output