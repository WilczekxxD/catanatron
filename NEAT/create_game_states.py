from typing import Iterable
from catanatron.models.actions import Action
from catanatron.models.player import Player


# creates a list of states after every legal move
def create_game_states(game, playable_actions):
    states = []
    for playable_action in playable_actions:
        game_copy = game.copy()
        game_copy.execute(playable_action)
        states.append(game_copy.state)

    return states
