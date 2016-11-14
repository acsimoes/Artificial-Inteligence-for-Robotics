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
grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
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

def path_grid(path_map, initial_position, final_position, grid):

    path = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    path[final_position[0]][final_position[1]] = '*'
    current_x = final_position[0]
    current_y = final_position[1]

    initial_x = initial_position[0]
    initial_y = initial_position[1]

    print initial_position
    while current_x != initial_x or current_y != initial_y:

        (previous_x, previous_y) = path_map[(current_x, current_y)]

        if(previous_x == current_x-1):
            path[previous_x][previous_y] = 'v'
        elif(previous_x == current_x+1):
            path[previous_x][previous_y] = '^'
        elif (previous_y == current_y + 1):
            path[previous_x][previous_y] = '<'
        else:
            path[previous_x][previous_y] = '>'

        current_x = previous_x
        current_y = previous_y

    print_grid(path)

    return path

def optimum_policy(grid,goal,cost):

    grid_rows = len(grid)
    grid_cols = len(grid[0])
    value = [[grid[col][row]*99 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    policy[goal[0]][goal[1]] = '*'

    open = [[0, goal[0], goal[1]]]
    end = False
    # path_map = {}
    while not end:

        # selected_position position with lowest cost
        min_value = float("inf")
        selected = []  # position selected for expansion
        for i in range(len(open)):
            x = open[i][1]
            y = open[i][2]
            g = open[i][0]
            if (min_value > g):
                min_value = g
                ind = i
                selected = open[i]

        del open[ind]
        x2 = selected[1]
        y2 = selected[2]
        g2 = selected[0]
        if(g2 == 0):
            value[x2][y2] = 1
        else:
            value[x2][y2] = g2

        #expand this position
        for i in range(len(delta)):
            x3 = x2 + delta[i][0]
            y3 = y2 + delta[i][1]
            g3 = g2 + cost
            # check if whether position is possible (not out of bounds or inside obstacles)
            if (min((x3, y3)) >= 0 and x3 < grid_rows and y3 < grid_cols):
                if (value[x3][y3] == 0):
                    # add to open
                    policy[x3][y3] = delta_name[(i+2)%4]
                    open.append((g3, x3, y3))
                    #path_map[(x3, y3)] = (x2, y2)

        if(len(open) == 0):
            end = True
            for x in range(grid_rows):
                for y in range(grid_cols):
                    if value[x][y] == 0:
                        value[x][y] = 99
            value[goal[0]][goal[1]] = 0

    return policy


def search(grid, init, goal, cost):
    grid_rows = len(grid)
    grid_cols = len(grid[0])
    open = [[0, init[0], init[1]]]
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
        selected = []               # position selected for expansion

        for i in range(len(open)):
            x = open[i][1]
            y = open[i][2]
            g = open[i][0]
            if (min_value > g):
                min_value = g
                ind = i
                selected = open[i]

        del open[ind]
        x2 = selected[1]
        y2 = selected[2]
        g2 = selected[0]
        expand[x2][y2] = count
        count += 1

        # expand this postion
        for i in range(len(delta)):
            x3 = x2 + delta[i][0]
            y3 = y2 + delta[i][1]
            g3 = g2 + cost

            #check if whether position is possible (not out of bounds or inside obstacles)
            if(min((x3,y3)) >= 0 and x3 < grid_rows and y3 < grid_cols):
                if(aux_grid[x3][y3] == 0):

                    #check whether it is at goal
                    if([x3, y3] == goal):
                        print 'Reached Goal!'
                        path = (g3, x3, y3)
                        expand[x3][y3] = count
                        found = True
                        path_map[(x3, y3)] = (x2, y2)
                        path_grid(path_map, init, goal,aux_grid)
                    else:
                        #add next_position to the open_position
                        aux_grid[x3][y3] = 2
                        open.append((g3, x3, y3))
                        path_map[(x3, y3)] = (x2, y2)

        if(len(open) == 0 and not found):     # no more possible moves and not at goal
            path = 'fail'
            resign = True


    print_grid(expand)
    return path

print search(grid,init,goal,cost)
print_grid(optimum_policy(grid,goal,cost))
