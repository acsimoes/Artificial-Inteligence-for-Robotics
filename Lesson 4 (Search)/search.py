# ----------
# User Instructions:
#
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

import math
import time

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']

def print_grid(grid):
    grid_rows = len(grid)
    grid_cols = len(grid[0])
    for i in range(grid_rows):
        print grid[i]

def print_path(path_map, initial_position, final_position, grid):

    path_grid = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    path_grid[final_position[0]][final_position[1]] = '*'
    current_x = final_position[0]
    current_y = final_position[1]

    initial_x = initial_position[0]
    initial_y = initial_position[1]

    print initial_position
    while current_x != initial_x or current_y != initial_y:

        (previous_x, previous_y) = path_map[(current_x, current_y)]

        if(previous_x == current_x-1):
            path_grid[previous_x][previous_y] = 'v'
        elif(previous_x == current_x+1):
            path_grid[previous_x][previous_y] = '^'
        elif (previous_y == current_y + 1):
            path_grid[previous_x][previous_y] = '<'
        else:
            path_grid[previous_x][previous_y] = '>'

        current_x = previous_x
        current_y = previous_y

    print_grid(path_grid)


def search(grid, init, goal, cost):
    grid_rows = len(grid)
    grid_cols = len(grid[0])
    open_position = [[0, init[0], init[1]]]
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    aux_grid = grid[:]              #auxiliary Grid that will have 2 on positions already visited
    aux_grid[init[0]][init[1]] = 2

    path = []
    resign = False
    found = False
    count = 0
    path_map = {}
    while not found and not resign:
        # selected_position position with lowest cost
        min_value = float("inf")
        selected_position = []

        for i in range(len(open_position)):
            if (min_value > open_position[i][0]):
                min_value = open_position[i][0]
                ind = i
                selected_position = open_position[i]

        del open_position[ind]
        expand[selected_position[1]][selected_position[2]] = count
        count += 1

        # expand this postion
        for i in range(len(delta)):
            next_position = [a + b for a, b in zip(delta[i], selected_position[1:])]

            #check if whether position is possible (not out of bounds or inside obstacles
            if(min(next_position) >= 0 and next_position[0] < grid_rows and next_position[1] < grid_cols):
                if(aux_grid[next_position[0]][next_position[1]] == 0):
                    next_position.insert(0, selected_position[0]+cost)

                    #check whether it is at goal
                    if(next_position[1:] == goal):
                        print 'Reached Goal!'
                        path = next_position
                        found = True
                        path_map[(next_position[1], next_position[2])] = (selected_position[1], selected_position[2])
                        print_path(path_map, init, goal,aux_grid)

                    #add next_position to the open_position
                    aux_grid[next_position[1]][next_position[2]] = 2
                    open_position.append(next_position)
                    path_map[(next_position[1], next_position[2])] = (selected_position[1], selected_position[2])


        if(len(open_position) == 0 and not found):     # no more possible moves and not at goal
            path = 'fail'
            resign = True

    expand[path[1]][path[2]] = count
    print_grid(expand)
    return path

print search(grid,init,goal,cost)
