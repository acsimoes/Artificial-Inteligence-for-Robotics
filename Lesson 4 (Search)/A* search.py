# -----------
# User Instructions:
#
# Modify the the search function so that it becomes
# an A* search algorithm as defined in the previous
# lectures.
#
# Your function should return the expanded grid
# which shows, for each element, the count when
# it was expanded or -1 if the element was never expanded.
#
# If there is no path from init to goal,
# the function should return the string 'fail'
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
heuristic = [[9, 8, 7, 6, 5, 4],
             [8, 7, 6, 5, 4, 3],
             [7, 6, 5, 4, 3, 2],
             [6, 5, 4, 3, 2, 1],
             [5, 4, 3, 2, 1, 0]]

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

def search(grid, init, goal, cost, heuristic):
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
            f = g + heuristic[x][y]
            if (min_value > f):
                min_value = f
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
                        print_path(path_map, init, goal,aux_grid)
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

print search(grid,init,goal,cost,heuristic)