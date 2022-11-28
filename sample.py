import neat.nn

import NEAT.restore
from catanatron import Game, RandomPlayer, Color
from NEAT.restore import read_model
from catanatron_experimental.my_player import MyPlayer
from catanatron_server.utils import open_link
from NEAT.neat_env import NeatEnv

config_path = "NEAT_config.txt"
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

ge = NEAT.restore.read_model("winner")
net = neat.nn.FeedForwardNetwork.create(ge, config)


# Play a simple 4v4 game. Edit MyPlayer with your logic!
players = [
    MyPlayer(ge, net, neat_env=0, color=Color.RED),
    RandomPlayer(Color.BLUE),
    RandomPlayer(Color.WHITE),
    RandomPlayer(Color.ORANGE),
]
wins = 0
for _ in range(25):
    game = Game(players)
    neat_env = NeatEnv(game)
    players[0].neat_env = neat_env
    color = game.play()  # returns winning color
    if color == Color.RED:
        wins += 1


# Ensure you have `docker-compose up` running
#   in another terminal tab:
# open_link(game)  # opens game result in browser