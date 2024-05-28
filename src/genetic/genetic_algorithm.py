from genetic.neural_network import NeuralNetwork
from game import Game
import numpy as np


class GeneticAlgorithm:
    
	NB_GENERATIONS = 100
    
	def __init__(self, population_size: int):
		self.__population = [NeuralNetwork() for _ in range(population_size)]
	
	def train(self):
		for generation in range(GeneticAlgorithm.NB_GENERATIONS):
			print(f"Generation {generation}")
			scores = self.__evaluate_population()
			parents = self.__select_parents(scores)
			self.__next_generation(parents)
			print(f"Max Score = {max(scores)}\n")
		print("Training finished")

	def __evaluate_population(self):
		game = Game()
		game.add_players(len(self.__population))
		players = game.get_players()
		game.start()

		while not game.is_game_over():
			for i, network in enumerate(self.__population):
				player = players[i]
				if not player.is_game_over():
					params = [
						# player.get_position()[1],  # vertical position
						player.get_y_velocity(),  # vertical velocity
         				player.get_horizontal_distance_next_pipe(),  # horizontal distance to next pipe
             			player.get_vertical_distance_next_pipe(),  # vertical distance to next pipe gap center
						# game.get_world().get_next_pipe().get_gap(),  # gap size
						# player.get_distance_to_ceil(),  # distance to ceil
						# player.get_distance_to_floor()  # distance to floor
                	]
					if network.predict(params):
						player.jump()
			game.update()

		return list(map(lambda player: player.get_score(), players))

	def __select_parents(self, scores):
		sorted_population = [network for _, network in sorted(zip(scores, self.__population), key=lambda pair: pair[0], reverse=True)]
		return sorted_population[:len(self.__population) // 2]

	def __next_generation(self, parents):
		children = parents[:len(parents) // 2]
  
		for i in range(len(parents) // 2):
			parent1, parent2 = parents[i], parents[-i - 1]
			for _ in range(2):
				child = NeuralNetwork.from_parents(parent1, parent2)
				child.mutate()
				children.append(child)

		while len(children) < len(self.__population):
			child = NeuralNetwork()
			children.append(child)
  
		self.__population = children