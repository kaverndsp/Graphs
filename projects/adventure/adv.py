from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack, Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

#Nodes: Rooms
# Edges: Exits leading to other rooms
# Fill this out with directions to walk

# Plan
# Do a DFT to get to an exit/end
# Append DFT path to traversal path
# When end is hit, Backtrack until unexplored node/room is found
# Append backtrack to traversal path
# Continue DFT to continue the traverse
# Rinse and repeat

# traversal_path = ['n', 'n']
traversal_path = []


def bfs(current_room, visited_rooms):
    # creates empty list of valid exits
    valid_exits = []
    # Creates list with all exits
    for exit in current_room.get_exits():
        # if the current room has not been visited
        if room_graph[current_room.id][1][exit] not in visited_rooms:
            # mark as visited and add the exit
            valid_exits.append(exit)
    # print(valid_exits)
    # return the updated valid exits
    return valid_exits


def traverse_rooms():

    # creates empty set of visted rooms
    visited_rooms = set()

    # adds the player's current room to the set
    visited_rooms.add(player.current_room.id)

    # list to reverse the path out of the room
    backwards_path = []

    # while loops the length of the visted rooms
    while len(visited_rooms) < len(room_graph):
        # sets the player in the current room
        current_room = player.current_room.id

        # bfs to get valid exits
        valid_exits = bfs(
            player.current_room, visited_rooms)

        # if there are no valid exits go backwards
        if len(valid_exits) == 0:
            # removes the last path used
            exit_direction = backwards_path.pop()
            player.travel(exit_direction)
            # adds the exit_direction/path from room
            traversal_path.append(exit_direction)
            continue

        # if the room hasn't been visited
        for exit_direction in valid_exits:
            # add the current room to visited
            visited_rooms.add(room_graph[current_room][1][exit_direction])

            # adds the exit_direction/path
            traversal_path.append(exit_direction)

            # the backwards path conversion
            if exit_direction == "n":
                backwards_path.append("s")
            elif exit_direction == "s":
                backwards_path.append("n")
            elif exit_direction == "w":
                backwards_path.append("e")
            else:
                backwards_path.append("w")
            player.travel(exit_direction)
            break


traverse_rooms()


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
