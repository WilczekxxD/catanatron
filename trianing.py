from catanatron import Game, RandomPlayer, Color
from catanatron_experimental.my_player import MyPlayer
from catanatron_server.utils import open_link
import os
import neat
from NEAT.neat_env import NeatEnv


def main(genomes, config):
    # Play a simple 4v4 game. Edit MyPlayer with your logic!
    nets = []
    ge = []
    for id, g in genomes:
        # setting up genomes, connecting them and appending to the genome list named ge

        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

    colors = [Color.RED, Color.BLUE, Color.WHITE, Color.ORANGE]
    players = [MyPlayer(genome, net, 0, color) for genome, net, color in zip(ge, nets, colors)]
    game = Game(players)
    neat_env = NeatEnv(game)
    for player in players:
        player.neat_env = neat_env

    print(game.play())  # returns winning color

    # Ensure you have `docker-compose up` running
    #   in another terminal tab:
    # open_link(game)  # opens game result in browser


def run(config_path):
    # those match the topic in configuration file, those names down there,
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    # showing stats instead of black running screan
    p.add_reporter(neat.Checkpointer(60))
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 1)
    # print('\nBest genome:\n{!s}'.format(winner))
    return winner, p.config


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'NEAT_config.txt')
    run(config_path)
