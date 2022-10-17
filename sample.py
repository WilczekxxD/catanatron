from catanatron import Game, RandomPlayer, Color
from catanatron_experimental.my_player import MyPlayer
from catanatron_server.utils import open_link
import os


def main(genomes, config):
    # Play a simple 4v4 game. Edit MyPlayer with your logic!
    players = [
        RandomPlayer(Color.RED),
        RandomPlayer(Color.BLUE),
        RandomPlayer(Color.WHITE),
        RandomPlayer(Color.ORANGE),
    ]
    game = Game(players)
    print(game.play())  # returns winning color

    # Ensure you have `docker-compose up` running
    #   in another terminal tab:
    # open_link(game)  # opens game result in browser


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'NEAT_config.txt')
    main(0, 0)
    #run(config_path)
