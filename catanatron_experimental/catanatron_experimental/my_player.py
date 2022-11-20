from typing import Iterable
from catanatron.game import Game
from catanatron.models.actions import Action
from catanatron.models.player import Player
import numpy as np


class MyPlayer(Player):

    def __init__(self, genome, net, neat_env, color, is_bot=True,):
        super().__init__(color, is_bot)
        self.genome = genome
        self.net = net
        self.neat_env = neat_env

    def decide(self, game: Game, playable_actions: Iterable[Action]):

        vectors = self.neat_env.game_to_vector(playable_actions)
        ratings = []
        for vector in vectors:
            rating = self.net.activate(vector)
            ratings.append(rating)

        id = np.argmax(ratings)
        return playable_actions[id]
