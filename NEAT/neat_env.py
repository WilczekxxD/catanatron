from NEAT.create_game_states import create_game_states
from NEAT.states_to_vector import generate_edge_list, state_to_vector


class NeatEnv:

    def __init__(self, game):
        self.game = game
        self.color_dictionary = self.create_color_dic()
        self.edge_list = generate_edge_list(self.game.state)

    def create_color_dic(self):
        color_dictionary = {}
        colors = self.game.state.colors
        for current in colors:
            color_int = {}
            counter = 1
            for color in colors:
                if color != current:
                    color_int[color] = str(counter)
                    counter += 1
                else:
                    color_int[color] = "0"
            color_dictionary[current] = color_int
        return color_dictionary

    def game_to_vector(self, playable_actions):
        color_int = self.color_dictionary[self.game.state.current_color()]
        states = create_game_states(self.game, playable_actions)

        vectors = []
        for state in states:
            vectors.append(state_to_vector(state, color_int, self.edge_list))

        return vectors
