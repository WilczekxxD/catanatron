import copy
import collections
from catanatron.state_functions import player_key, get_played_dev_cards
import networkx as nx
from catanatron.models.board import STATIC_GRAPH
'''
there are basicly 2 ways of describing the map
1. make an elaborate scheme of encoding state of every intersection, a nit like with tiles, based on:
~ by whom can it be accessed (which describes roads basicly)
~ whats built on them
~ is there a port

+ has few inputs 54 to be exact
- might be confusing for the net
- thinking of a consistent non repeating way of describing properties of nodes minimising number of different
possible values is hard

2. make it by who owns what in every kind of property, ownership based
~ for ports  9 inputs
~ for roads 72 inputs
~ for intersections/nodes 54

+ easier to implement
+ probably wont confuse the network that much
- has more inputs

breakdown of inputs for 2 scenario:

method of vectorising fields:
author uses https://math.stackexchange.com/questions/2254655/hexagon-grid-coordinate-system
to describe every field with (3,1) vector, ex(-1, 0, 1) where (0, 0, 0) is the center field
instead of this it will be easier to use indexes

every field is decribed like 10RESOURCE,
since every fields has two values it will be broken down into 2 ints
number will stay the number but resources will be changed according to this table           19 inputs
        # 0 - wheat
        # 1 - sheep
        # 2 - wood
        # 3 - brick
        # 4 - ore
        # 5 - desert
idea to keep in mind one can make twice the amount of inputs and first describe the numbers than the resources

state of ROBBER will be changed from the (3,1) vector to the int value
of the field in the list of fields it stays on                                                  1 input

buildings:                                                                                      54 inputs
list of intersections and marked by color which of them is built and what is built

ports:                                                                                          9 inputs
list of ports and their ownership

roads:                                                                                          72 inputs
list of edges with roads marked

hand:                                                                                           10 inputs        
wood
brick
sheep
wheat
ore
year of plenty
monopoly
vp
knights
road building


resources in bank:                                                                               6 inputs
wood
brick
sheep
wheat
ore
dev

played dev cards:                                                                                5 inputs
year of plenty
monopoly
vp
knights
road building

win conditions:                                                                                  12 inputs
points * 4
road lengths * 4
armies * 4
'''

resource_to_number = {
    "WOOD": 0,
    "BRICK": 1,
    "SHEEP": 2,
    "WHEAT": 3,
    "ORE": 4,
}

dev_to_number = {
    "YEAR_OF_PLENTY": 0,
    "MONOPOLY": 1,
    "VICTORY_POINT": 2,
    "KNIGHT": 3,
    "ROAD_BUILDING": 4
}


def state_to_vector(state):
    # tile vector (19,1)
    tile_vectors = tiles_to_vector(state)
    # robber vector int, (1, 1)
    robber_vector = robber_to_vector(state)

    # getting colors to numbers can be done ones a game for every player instead here for now
    current_color = state.current_player().color
    color_int = {}
    colors = state.colors.value
    counter = 1
    for color in colors:
        if color != current_color:
            color_int[color] = str(counter)
            counter += 1
        else:
            color_int[color] = "0"

    # buildings (54, 1)
    buildings_vector = buildings_to_vector(state, color_int)

    # ports (9, 1)
    ports_vector = ports_to_vector(state, buildings_vector)

    # roads (72, 1)
    edge_list = generate_edge_list(state)
    roads_vector = roads_to_vector(state, edge_list, color_int)

    # resources in hand:


def tiles_to_vector(state):
    # field
    # this whole section ca be done once a game
    tiles = state.board.map.land_tiles
    tile_vectors = []
    for tile in tiles.values():
        tile_number = tile.number
        if not tile_number:
            tile_number = 5
        tile_resource = tile.resource
        if tile_resource:
            tile_resource = resource_to_number[tile_resource]
        else:
            tile_resource = 5

        tile_vector = int(str(tile_number) + str(tile_resource))
        tile_vectors.append(tile_vector)

    return tile_vectors


def robber_to_vector(state):
    # robber
    robber_vector = []
    robber = state.board.robber_coordinate
    robber_index = list(state.board.map.land_tiles).index(robber)
    robber_vector.append(robber_index)
    return robber_vector


def buildings_to_vector(state, color_dictionary):
    # buildings

    building_int = {
        'SETTLEMENT': "1",
        'CITY': "2"
    }

    intersections_vector = [-1 for _ in range(54)]
    buildings_dict = state.board.buildings
    for id in buildings_dict:
        values = buildings_dict[id]
        color = color_dictionary[values[0]]
        building = building_int[values[1]]
        # case can be made for color * building instead of + but then current player has to be 1
        int_field = int(building + color)
        intersections_vector[id] = int_field

    return intersections_vector


def ports_to_vector(state, buildings_vector):
    ports_vector = [-1 for _ in range(9)]
    # coping
    port_nodes = copy.copy(state.board.map.port_nodes)
    # changin None key to str "ANone" to sort it since None can not be comapred with string
    port_nodes["None"] = port_nodes.pop(None)
    # sorting
    port_nodes = collections.OrderedDict(sorted(port_nodes.items()))
    # giving the None back
    port_nodes[None] = port_nodes.pop("None")
    print(port_nodes.keys())
    for j, key in enumerate(port_nodes):
        port_type_nodes = port_nodes[key]
        for i in range(len(port_type_nodes)//2):
            owner = -1
            list_port_type_nodes = list(port_type_nodes)
            single_port_nodes = [list_port_type_nodes[i * 2], list_port_type_nodes[i * 2 + 1]]
            for node in single_port_nodes:
                building = buildings_vector[node]
                # print(building)
                if building > -1:
                    if (building % 10) == 0:
                        owner = 0
                    else:
                        owner = int(str(building)[-1])
                    break
            ports_vector[j+i] = owner

    return ports_vector


def roads_to_vector(state, edge_list, color_dictionary):
    # mapping roads to vector using the same color encoding as previously
    roads_vector = [-1 for _ in range(72)]
    roads = state.board.roads
    for edge, color in roads.items():
        index = edge_list.index(edge)
        int_color = color_dictionary[color]
        roads_vector[index] = int_color

    return roads_vector


def generate_edge_list(state):
    # going for every tile, adding one edge at a time checking if it alreqady is there
    edge_list = []
    land_tiles = state.board.map.land_tiles
    for position, tile in land_tiles.items():
        edges = tile.edges
        for edge in edges.values():
            if edge not in edge_list:
                edge_list.append(edge)

    return edge_list


def hand_to_vector(state):
    hand_vector = [0 for _ in range(10)]
    color = state.current_player().color
    key = player_key(state, color)
    for resource, value in resource_to_number.items():
        hand_vector[value] = state.player_state[f"{key}_{resource}_IN_HAND"]
    for dev, value in dev_to_number.items():
        hand_vector[value + 5] = state.player_state[f"{key}_{dev}_IN_HAND"]

    return hand_vector


def used_devs_to_vector(state):
    colors = state.colors
    keys = [player_key(state, color) for color in colors]
    used_devs_vector = [0 for _ in range(5)]
    for key in keys:
        for dev, value in dev_to_number.items():
            used_devs_vector[value] += state.player_state[f"{key}_PLAYED_{dev}"]

    return used_devs_vector
