from typing import Iterable

from catanatron.game import Game
from catanatron.models.actions import Action
from catanatron.models.player import Player


class MyPlayer(Player):
    def decide(self, game: Game, playable_actions: Iterable[Action]):





        # for the sake of testing
        return playable_actions[0]

