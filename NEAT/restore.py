from catanatron import Game, RandomPlayer, Color
from catanatron_experimental.my_player import MyPlayer
from catanatron_server.utils import open_link
import os
import neat
from NEAT.neat_env import NeatEnv
import gzip
import pickle


def read_generation(checkpoint, config_path, fitness_function):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Checkpointer.restore_checkpoint(checkpoint)

    return p.run(fitness_function, 1)


def read_model(file_name):
    with gzip.open(file_name) as f:
        obj = pickle.load(f)
        return obj


def save_model(model, file_name):
    with gzip.open(file_name, 'w', compresslevel=5) as f:
        pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)

