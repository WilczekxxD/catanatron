'''
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


win conditions                                                                               4 inputs
points
road lengths
armies


What is written above might not be true
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
'''

import copy
import collections

resource_to_number = {
    "WHEAT": 0,
    "SHEEP": 1,
    "WOOD": 2,
    "BRICK": 3,
    "ORE": 4,
}


def state_to_vector(state):
    tile_vectors = tiles_to_vector(state)
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
    building_vector = buildings_to_vector(state, color_int)
    # intersections

    intersections_vector = [-1 for _ in range(54)]
    # not sure if will work since no idea when current player changes
    # TODO: find this place and make sure its not after executing a command
    current_color = state.current_player().color
    # getting colors to numbers can be done ones a game for every player instead
    color_int = {}
    colors = state.colors.value
    counter = 1
    for color in colors:
        if color != current_color:
            color_int[color] = str(counter)
            counter += 1
        else:
            color_int[color] = "0"

    # marking connected
    connected_components = state.board.connected_components[current_color]
    for subgraph in connected_components:
        for component in subgraph:
            intersections_vector.insert(component, 0)

    # ports
    ports_vector = [-1 for _ in range(9)]
    ports = state.board.player_port_resources_cache


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
        int_field = int(color+building)
        intersections_vector.pop(id)
        intersections_vector.insert(id, int_field)

    return intersections_vector


def ports_to_vector(state, buildings_vector):
    ports_vector = [-1 for _ in range(9)]
    # coping
    port_nodes = copy.copy(state.board.map.port_nodes)
    # changin None key to str "ANone" to sort it and for it to be first
    port_nodes["ANone"] = port_nodes.pop(None)
    # sorting
    port_nodes = collections.OrderedDict(sorted(port_nodes.items()))
    # giving the None back
    port_nodes[None] = port_nodes.pop("ANone")
    print(port_nodes.keys())
    for j, key in enumerate(port_nodes):
        port_type_nodes = port_nodes[key]
        for i in range(len(port_type_nodes)//2):
            owner = -1
            list_port_type_nodes = list(port_type_nodes)
            single_port_nodes = [list_port_type_nodes[i * 2], list_port_type_nodes[i * 2 + 1]]
            for node in single_port_nodes:
                building = buildings_vector[node]
                #print(building)
                if building > -1:
                    if (building // 10) == 0:
                        owner = 0
                    else:
                        owner = int(str(building)[0])
                    break
            ports_vector[j+i] = owner

    return ports_vector




