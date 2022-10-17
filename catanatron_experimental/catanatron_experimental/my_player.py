from typing import Iterable

from catanatron.game import Game
from catanatron.models.actions import Action
from catanatron.models.player import Player


class MyPlayer(Player):

    def __init__(self, color, genome, net, is_bot=True,):
        super().__init__(color, is_bot)
        self.genome = genome
        self.net = net

    def decide(self, game: Game, playable_actions: Iterable[Action]):


        # for the sake of testing
        return playable_actions[0]

