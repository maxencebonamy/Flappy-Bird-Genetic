# from game import Game

# game = Game()

# while True:
# 	game.update()

from genetic import GeneticAlgorithm

algo = GeneticAlgorithm(1000)
algo.train()