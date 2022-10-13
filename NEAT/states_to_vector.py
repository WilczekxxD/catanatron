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
        # 4 - stone
        # 5 - desert

state of ROBBER will be changed from the vector to the index
of field in the list of fields it stays on                                                  1 input

state of every intersaction is either something is there or not.                            54 inputs
if nothing there and inaacessible - -1
if nothing there and accessible - 0
if something is there:
opponents number + 1 for a settlement or 2 for city

TODO: DO I NEED STREETS? IF I GIVE THE ACCESSED PORTS AND ACCESSED INTERSECTIONS THERE IS NO NEED FOR

ports are described by name or NONE
9 ports so                                                                                   9 inputs
-1 for empty
5 for NONE (3:1)
0 for wheat port
1 for sheep port
2 for wood port
3 for brivk port
4 for stone

win conditions                                                                               4 inputs
points
road lengths
armies
'''

def state_to_vector(state):
    # field





